import asyncio
import asyncpg
import os
import json
from dotenv import load_dotenv

load_dotenv()

mock_news = [
    # ==========================================
    # --- 5 COINCIDENCIAS COMPLETAS (FULL MATCH) ---
    # ==========================================
    {
        "title": "Nginx updates stable branch to address critical buffer overflow",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-NGINX-BUF",
        "rawcontent": "A buffer overflow vulnerability has been discovered in the Nginx HTTP/2 module. It affects Nginx HTTP/2 implementation in versions 1.18.0 and earlier. An attacker can exploit this to achieve remote code execution (RCE).",
        "tags": {
            "cve_id": "CVE-2024-NGINX-BUF",
            "severidad": "Crítico",
            "activos_afectados": {"nginx": ["<=1.18.0"]},
            "acción_recomendada": "Upgrade Nginx immediately to version 1.18.1 or higher.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Buffer Overflow",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "PostgreSQL 15.2 vulnerable to database crash on recursive queries",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PG-CRASH",
        "rawcontent": "PostgreSQL versions in the 15.x branch up to 15.2 are vulnerable to a denial of service. Specific recursive queries with window functions can trigger a server crash, resulting in database unavailability.",
        "tags": {
            "cve_id": "CVE-2024-PG-CRASH",
            "severidad": "Alto",
            "activos_afectados": {"postgresql": ["==15.2.0"]},
            "acción_recomendada": "Upgrade to PostgreSQL 15.3.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Denial of Service",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Apache HTTP Server 2.4.49 path traversal vulnerability actively exploited",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41773",
        "rawcontent": "A path traversal vulnerability in Apache HTTP Server 2.4.49 allows attackers to read arbitrary files and, under certain configurations, execute remote code via server commands.",
        "tags": {
            "cve_id": "CVE-2021-41773",
            "severidad": "Crítico",
            "activos_afectados": {"apache": ["2.4.49"]},
            "acción_recomendada": "Upgrade to Apache HTTP Server 2.4.50 immediately.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Path Traversal",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Java SE Runtime Environment 8u181 and earlier privilege escalation",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JAVA-PRIV",
        "rawcontent": "A vulnerability in Oracle Java SE versions 8 (specifically 1.8.0 and earlier updates) allows local users to escalate privileges via the hotkey handler during runtime execution.",
        "tags": {
            "cve_id": "CVE-2024-JAVA-PRIV",
            "severidad": "Alto",
            "activos_afectados": {"java": ["<=1.8.0"]},
            "acción_recomendada": "Upgrade Java to runtime update 201 or newer.",
            "puntuacion_cvss": "7.8",
            "tipo_vulnerabilidad": "Privilege Escalation",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Python 3.10.x SSL module vulnerability allows certificate bypass",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PY-SSL",
        "rawcontent": "Python 3.10.4 and all versions in the 3.10 branch prior to 3.10.5 contain a vulnerability in the ssl module. Under specific circumstances, certificate revocation checks are bypassed, enabling man-in-the-middle attacks.",
        "tags": {
            "cve_id": "CVE-2024-PY-SSL",
            "severidad": "Medio",
            "activos_afectados": {"python": ["<=3.10.4"]},
            "acción_recomendada": "Upgrade to Python 3.10.5 or newer.",
            "puntuacion_cvss": "6.5",
            "tipo_vulnerabilidad": "Cryptographic Bypass",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },

    # ==========================================
    # --- 10 COINCIDENCIAS PARCIALES (PARTIAL MATCH) ---
    # ==========================================
    {
        "title": "Nginx 1.25.x / 1.26.x HTTP/3 Rapid Reset vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-NGINX-H3",
        "rawcontent": "A denial of service vulnerability in Nginx 1.25.x and 1.26.x HTTP/3 implementation allows remote attackers to cause high CPU usage via HTTP/3 requests.",
        "tags": {
            "cve_id": "CVE-2024-NGINX-H3",
            "severidad": "Medio",
            "activos_afectados": {"nginx": ["1.25.x", "1.26.x"]},
            "acción_recomendada": "Upgrade Nginx to version 1.27 stable.",
            "puntuacion_cvss": "5.3",
            "tipo_vulnerabilidad": "Denial of Service",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Python 3.11/3.12 integer overflow in tarfile module",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PY-TAR",
        "rawcontent": "An integer overflow vulnerability exists in Python versions >=3.11.0 when parsing malicious tar files, leading to memory corruption.",
        "tags": {
            "cve_id": "CVE-2024-PY-TAR",
            "severidad": "Alto",
            "activos_afectados": {"python": [">=3.11.0"]},
            "acción_recomendada": "Update Python installation to the latest patch release.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Integer Overflow",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "PostgreSQL 14 security update fixes SQL injection in extensions",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PG-SQLI",
        "rawcontent": "PostgreSQL 14.x contains a vulnerability in its extension manager that allows database administrators to execute arbitrary SQL commands.",
        "tags": {
            "cve_id": "CVE-2024-PG-SQLI",
            "severidad": "Alto",
            "activos_afectados": {"postgresql": ["14.x"]},
            "acción_recomendada": "Update to PostgreSQL 14.10 or newer.",
            "puntuacion_cvss": "7.2",
            "tipo_vulnerabilidad": "SQL Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Apache HTTP Server 2.4.58 HTTP/2 Denial of Service",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-APACHE-H2",
        "rawcontent": "A vulnerability in Apache HTTP Server 2.4.58 allows an attacker to exhaust server resources using HTTP/2 stream multiplexing.",
        "tags": {
            "cve_id": "CVE-2024-APACHE-H2",
            "severidad": "Medio",
            "activos_afectados": {"apache": [">=2.4.58"]},
            "acción_recomendada": "Update Apache HTTP Server to version 2.4.59.",
            "puntuacion_cvss": "6.0",
            "tipo_vulnerabilidad": "Denial of Service",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Oracle Java SE 17 / 21 Remote Code Execution vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JAVA-RCE",
        "rawcontent": "A critical vulnerability in Oracle Java SE versions 17.x and 21.x allows remote attackers to execute arbitrary code via the Java 2D component.",
        "tags": {
            "cve_id": "CVE-2024-JAVA-RCE",
            "severidad": "Crítico",
            "activos_afectados": {"java": ["==17.*", "==21.*"]},
            "acción_recomendada": "Apply the Java CPU update released in Oracle security advisory.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Remote Code Execution",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Nginx 1.20.2 memory leak in SSL handshake",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-NGINX-LEAK",
        "rawcontent": "Nginx version 1.20.2 contains a memory leak vulnerability during SSL/TLS handshake negotiations when keeping connection alive.",
        "tags": {
            "cve_id": "CVE-2024-NGINX-LEAK",
            "severidad": "Bajo",
            "activos_afectados": {"nginx": ["1.20.2"]},
            "acción_recomendada": "Update Nginx to the current branch.",
            "puntuacion_cvss": "3.5",
            "tipo_vulnerabilidad": "Memory Leak",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Python 3.12.x arbitrary code execution in urllib",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PY-URL",
        "rawcontent": "A vulnerability in Python 3.12.x urllib module allows arbitrary command execution via crafted URL schemes parsed by the script parser.",
        "tags": {
            "cve_id": "CVE-2024-PY-URL",
            "severidad": "Alto",
            "activos_afectados": {"python": ["3.12.x"]},
            "acción_recomendada": "Update Python environment to the latest 3.12 version.",
            "puntuacion_cvss": "8.8",
            "tipo_vulnerabilidad": "Remote Code Execution",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "PostgreSQL 12.x buffer overflow in pg_dump tool",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PG-DUMP",
        "rawcontent": "PostgreSQL 12.x database backups using the pg_dump utility are vulnerable to stack-based buffer overflows when exporting very long table names.",
        "tags": {
            "cve_id": "CVE-2024-PG-DUMP",
            "severidad": "Medio",
            "activos_afectados": {"postgresql": ["12.x"]},
            "acción_recomendada": "Update to PostgreSQL 12.15.",
            "puntuacion_cvss": "5.5",
            "tipo_vulnerabilidad": "Buffer Overflow",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Apache HTTP Server 2.4.52 vulnerability allows request smuggling",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-APACHE-SMUGGLE",
        "rawcontent": "A request smuggling vulnerability exists in Apache HTTP Server version 2.4.52 when handling invalid Transfer-Encoding headers in a proxy configuration.",
        "tags": {
            "cve_id": "CVE-2024-APACHE-SMUGGLE",
            "severidad": "Alto",
            "activos_afectados": {"apache": ["2.4.52"]},
            "acción_recomendada": "Update Apache Server binary.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Request Smuggling",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Oracle Java SE 11.x vulnerability in security handshake",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JAVA-TLS",
        "rawcontent": "A vulnerability in Java SE 11.x TLS negotiation allows unauthorized read access to secure streams during the key exchange handshake.",
        "tags": {
            "cve_id": "CVE-2024-JAVA-TLS",
            "severidad": "Medio",
            "activos_afectados": {"java": ["11.*"]},
            "acción_recomendada": "Upgrade Java Runtime Environment.",
            "puntuacion_cvss": "5.3",
            "tipo_vulnerabilidad": "Information Disclosure",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },

    # ==========================================
    # --- 35 NO COINCIDEN (NO MATCH) ---
    # ==========================================
    {
        "title": "Kubernetes API Server vulnerability allows privilege escalation",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-K8S-PRIV",
        "rawcontent": "An escalation of privilege vulnerability has been identified in Kubernetes API Server. Remote users can bypass authentication under specific configurations.",
        "tags": {
            "cve_id": "CVE-2024-K8S-PRIV",
            "severidad": "Crítico",
            "activos_afectados": {"kubernetes": ["1.28.*"]},
            "acción_recomendada": "Upgrade Kubernetes Cluster.",
            "puntuacion_cvss": "9.0",
            "tipo_vulnerabilidad": "Privilege Escalation",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Docker Desktop arbitrary file write on Windows host",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-DOCKER-FILE",
        "rawcontent": "A vulnerability in Docker Desktop for Windows allows local users to write files to arbitrary locations with administrative privileges.",
        "tags": {
            "cve_id": "CVE-2024-DOCKER-FILE",
            "severidad": "Medio",
            "activos_afectados": {"docker_desktop": ["<=4.25.0"]},
            "acción_recomendada": "Update Docker Desktop to version 4.26.0.",
            "puntuacion_cvss": "6.8",
            "tipo_vulnerabilidad": "File Overwrite",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Linux Kernel privilege escalation in eBPF subsystem",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-LINUX-EBPF",
        "rawcontent": "A flaw in the eBPF subsystem in the Linux kernel allows local users to execute arbitrary code and gain root privileges due to incorrect validation.",
        "tags": {
            "cve_id": "CVE-2024-LINUX-EBPF",
            "severidad": "Alto",
            "activos_afectados": {"linux_kernel": ["<6.4.0"]},
            "acción_recomendada": "Recompile kernel with security fixes or upgrade to newer branch.",
            "puntuacion_cvss": "7.8",
            "tipo_vulnerabilidad": "Privilege Escalation",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Jenkins Server remote code execution in core controller",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JENKINS-RCE",
        "rawcontent": "A remote code execution vulnerability exists in Jenkins Server core controller when handling CLI command requests.",
        "tags": {
            "cve_id": "CVE-2024-JENKINS-RCE",
            "severidad": "Crítico",
            "activos_afectados": {"jenkins": ["<=2.440"]},
            "acción_recomendada": "Upgrade Jenkins to 2.441.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "GitLab security patch addresses critical account takeover vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-GITLAB-AUTH",
        "rawcontent": "An account takeover vulnerability has been patched in GitLab Community and Enterprise editions. It allows attackers to reset user passwords without verification.",
        "tags": {
            "cve_id": "CVE-2024-GITLAB-AUTH",
            "severidad": "Crítico",
            "activos_afectados": {"gitlab": ["<16.7.2"]},
            "acción_recomendada": "Update GitLab instances immediately.",
            "puntuacion_cvss": "10.0",
            "tipo_vulnerabilidad": "Account Takeover",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Redis Server denial of service via Lua scripts",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-REDIS-DOS",
        "rawcontent": "A denial of service vulnerability in Redis Server allows authorized clients to trigger an out-of-memory crash via specially crafted Lua scripts.",
        "tags": {
            "cve_id": "CVE-2024-REDIS-DOS",
            "severidad": "Medio",
            "activos_afectados": {"redis": ["<7.2.4"]},
            "acción_recomendada": "Upgrade Redis Server.",
            "puntuacion_cvss": "5.5",
            "tipo_vulnerabilidad": "DoS",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Memcached remote buffer overflow in memory management",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-MEMCACHED-BO",
        "rawcontent": "A buffer overflow in Memcached memory compression handler allows remote attackers to execute arbitrary code.",
        "tags": {
            "cve_id": "CVE-2024-MEMCACHED-BO",
            "severidad": "Alto",
            "activos_afectados": {"memcached": ["<=1.6.22"]},
            "acción_recomendada": "Update Memcached to version 1.6.23.",
            "puntuacion_cvss": "8.8",
            "tipo_vulnerabilidad": "Buffer Overflow",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Elasticsearch authorization bypass in Kibana dashboard",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-ES-KIBANA",
        "rawcontent": "An authorization bypass vulnerability in Kibana allows read-only users to perform search queries on restricted elasticsearch indexes.",
        "tags": {
            "cve_id": "CVE-2024-ES-KIBANA",
            "severidad": "Medio",
            "activos_afectados": {"kibana": ["<8.11.3"]},
            "acción_recomendada": "Upgrade Kibana and Elasticsearch deployment.",
            "puntuacion_cvss": "6.5",
            "tipo_vulnerabilidad": "Auth Bypass",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "MongoDB database engine privilege escalation on Linux",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-MONGO-PRIV",
        "rawcontent": "MongoDB Server on Linux environments is vulnerable to a local privilege escalation flaw in the storage driver interface.",
        "tags": {
            "cve_id": "CVE-2024-MONGO-PRIV",
            "severidad": "Alto",
            "activos_afectados": {"mongodb": ["<7.0.2"]},
            "acción_recomendada": "Update MongoDB to version 7.0.3.",
            "puntuacion_cvss": "7.2",
            "tipo_vulnerabilidad": "Privilege Escalation",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Node.js HTTP request smuggling vulnerability in llhttp parser",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-NODE-SMUGGLE",
        "rawcontent": "A request smuggling vulnerability exists in Node.js HTTP runtime due to parser laxness in the llhttp module.",
        "tags": {
            "cve_id": "CVE-2024-NODE-SMUGGLE",
            "severidad": "Alto",
            "activos_afectados": {"nodejs": ["<20.10.0"]},
            "acción_recomendada": "Upgrade Node.js.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Request Smuggling",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "PHP 8.2 critical remote code execution vulnerability in CGI mode",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-PHP-RCE",
        "rawcontent": "PHP 8.2 configurations running CGI mode are vulnerable to a remote command injection because of argument parsing flaws.",
        "tags": {
            "cve_id": "CVE-2024-PHP-RCE",
            "severidad": "Crítico",
            "activos_afectados": {"php": ["8.2.x", "8.3.x"]},
            "acción_recomendada": "Upgrade PHP to the latest security patch.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Zoom Client for Windows remote execution via chat attachments",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-ZOOM-EXEC",
        "rawcontent": "Zoom Client for Windows allows attackers to execute code on local host via maliciously crafted chat attachments.",
        "tags": {
            "cve_id": "CVE-2024-ZOOM-EXEC",
            "severidad": "Alto",
            "activos_afectados": {"zoom": ["<5.16.5"]},
            "acción_recomendada": "Upgrade Zoom application.",
            "puntuacion_cvss": "8.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Google Chrome updates stable channel to fix zero-day vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-CHROME-ZERO",
        "rawcontent": "Google has pushed a security update to address a zero-day vulnerability in Chrome V8 engine that is actively exploited.",
        "tags": {
            "cve_id": "CVE-2024-CHROME-ZERO",
            "severidad": "Alto",
            "activos_afectados": {"chrome": ["<120.0.6099.129"]},
            "acción_recomendada": "Relaunch Chrome to apply update.",
            "puntuacion_cvss": "8.8",
            "tipo_vulnerabilidad": "Use-After-Free",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Firefox browser address bar spoofing vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-FIREFOX-SPOOF",
        "rawcontent": "A vulnerability in Firefox allowed attackers to spoof the address bar contents via specifically formatted URL redirects.",
        "tags": {
            "cve_id": "CVE-2024-FIREFOX-SPOOF",
            "severidad": "Medio",
            "activos_afectados": {"firefox": ["<121.0"]},
            "acción_recomendada": "Upgrade Firefox.",
            "puntuacion_cvss": "5.3",
            "tipo_vulnerabilidad": "Spoofing",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "OpenSSL 3.1.2 Denial of Service in certificate validation",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-OPENSSL-NEW",
        "rawcontent": "OpenSSL 3.1.2 contains a vulnerability where parsing a certificate containing invalid parameters causes CPU exhaustion.",
        "tags": {
            "cve_id": "CVE-2024-OPENSSL-NEW",
            "severidad": "Medio",
            "activos_afectados": {"openssl": ["3.1.2"]},
            "acción_recomendada": "Update to OpenSSL 3.1.3.",
            "puntuacion_cvss": "5.3",
            "tipo_vulnerabilidad": "DoS",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "OpenSSH Server remote execution vulnerability in sshd",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-OPENSSH-RCE",
        "rawcontent": "A vulnerability in OpenSSH Server allow remote attackers to execute arbitrary code due to signal handler race conditions in sshd daemon.",
        "tags": {
            "cve_id": "CVE-2024-OPENSSH-RCE",
            "severidad": "Crítico",
            "activos_afectados": {"openssh": ["<9.8p1"]},
            "acción_recomendada": "Update OpenSSH immediately.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Apache Tomcat remote code execution via JSP upload",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-TOMCAT-RCE",
        "rawcontent": "Apache Tomcat configurations allowing file uploads are vulnerable to remote code execution through malicious JSP files execution.",
        "tags": {
            "cve_id": "CVE-2024-TOMCAT-RCE",
            "severidad": "Crítico",
            "activos_afectados": {"tomcat": ["<=9.0.83"]},
            "acción_recomendada": "Upgrade Apache Tomcat.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Oracle WebLogic Server deserialization vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-WEBLOGIC-JAVA",
        "rawcontent": "A remote code execution vulnerability exists in Oracle WebLogic Server due to unsafe Java object deserialization in console.",
        "tags": {
            "cve_id": "CVE-2024-WEBLOGIC-JAVA",
            "severidad": "Crítico",
            "activos_afectados": {"weblogic": ["12.2.1.4.0", "14.1.1.0.0"]},
            "acción_recomendada": "Apply Oracle WebLogic quarterly security update.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Red Hat JBoss Enterprise Application Server authentication bypass",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JBOSS-BYPASS",
        "rawcontent": "A vulnerability in Red Hat JBoss Enterprise Application Server allows remote administrators to bypass console authentication.",
        "tags": {
            "cve_id": "CVE-2024-JBOSS-BYPASS",
            "severidad": "Alto",
            "activos_afectados": {"jboss_eas": ["<7.4.12"]},
            "acción_recomendada": "Update JBoss Server configuration.",
            "puntuacion_cvss": "8.8",
            "tipo_vulnerabilidad": "Auth Bypass",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "IBM WebSphere Application Server XML External Entity vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-WAS-XXE",
        "rawcontent": "IBM WebSphere Application Server is vulnerable to XXE injections when parsing administrative configurations.",
        "tags": {
            "cve_id": "CVE-2024-WAS-XXE",
            "severidad": "Medio",
            "activos_afectados": {"websphere": ["8.5.5.*", "9.0.5.*"]},
            "acción_recomendada": "Apply WAS security fix packs.",
            "puntuacion_cvss": "6.5",
            "tipo_vulnerabilidad": "XXE Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Drupal Core security release fixes critical access bypass",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-DRUPAL-BYPASS",
        "rawcontent": "Drupal Core contains a vulnerability in its routing component allowing anonymous users to access restricted administrative resources.",
        "tags": {
            "cve_id": "CVE-2024-DRUPAL-BYPASS",
            "severidad": "Alto",
            "activos_afectados": {"drupal": ["<10.1.8"]},
            "acción_recomendada": "Update Drupal Core.",
            "puntuacion_cvss": "8.5",
            "tipo_vulnerabilidad": "Access Bypass",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "WordPress Plugin WooCommerce SQL injection vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-WP-WOO",
        "rawcontent": "A vulnerability in WooCommerce plugin for WordPress allow authenticated users to execute SQL commands in backend databases.",
        "tags": {
            "cve_id": "CVE-2024-WP-WOO",
            "severidad": "Alto",
            "activos_afectados": {"wordpress_plugin_woocommerce": ["<8.2.0"]},
            "acción_recomendada": "Upgrade WooCommerce immediately.",
            "puntuacion_cvss": "8.1",
            "tipo_vulnerabilidad": "SQL Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Joomla CMS vulnerability allows unauthorized database modification",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JOOMLA-DB",
        "rawcontent": "An API endpoint in Joomla CMS leaks database credentials under specific error handling conditions.",
        "tags": {
            "cve_id": "CVE-2024-JOOMLA-DB",
            "severidad": "Alto",
            "activos_afectados": {"joomla": ["<=4.4.1"]},
            "acción_recomendada": "Update Joomla to version 4.4.2.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Information Disclosure",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Roundcube Webmail cross-site scripting vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-ROUNDCUBE-XSS",
        "rawcontent": "A cross-site scripting (XSS) vulnerability in Roundcube webmail allows attackers to execute scripts via mail bodies.",
        "tags": {
            "cve_id": "CVE-2024-ROUNDCUBE-XSS",
            "severidad": "Medio",
            "activos_afectados": {"roundcube": ["<1.6.4"]},
            "acción_recomendada": "Update Roundcube installation.",
            "puntuacion_cvss": "6.1",
            "tipo_vulnerabilidad": "XSS",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Microsoft Outlook Remote Code Execution via preview pane",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-OUTLOOK-RCE",
        "rawcontent": "Microsoft Outlook contains a remote code execution vulnerability triggered when rendering emails in the preview pane.",
        "tags": {
            "cve_id": "CVE-2024-OUTLOOK-RCE",
            "severidad": "Crítico",
            "activos_afectados": {"outlook": ["<=2021"]},
            "acción_recomendada": "Apply Microsoft Update patches.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Cisco IOS XE Software command injection vulnerability in web UI",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-CISCO-XE",
        "rawcontent": "A command injection vulnerability in Cisco IOS XE Software web management UI allows remote attackers to execute OS commands.",
        "tags": {
            "cve_id": "CVE-2024-CISCO-XE",
            "severidad": "Crítico",
            "activos_afectados": {"cisco_ios_xe": ["17.*"]},
            "acción_recomendada": "Apply patch releases or disable HTTP Server interface.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Command Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Fortinet FortiOS SSL VPN remote code execution actively exploited",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-FORTINET-VPN",
        "rawcontent": "A critical vulnerability in Fortinet FortiOS SSL VPN daemon allows remote attackers to execute arbitrary code via HTTP headers.",
        "tags": {
            "cve_id": "CVE-2024-FORTINET-VPN",
            "severidad": "Crítico",
            "activos_afectados": {"fortios": ["<=7.2.4"]},
            "acción_recomendada": "Upgrade FortiOS instantly.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Juniper Networks Junos OS privilege escalation in SSH daemon",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-JUNIPER-SSH",
        "rawcontent": "A flaw in Juniper Networks Junos OS SSH configuration handler allows local users to escalate privileges.",
        "tags": {
            "cve_id": "CVE-2024-JUNIPER-SSH",
            "severidad": "Alto",
            "activos_afectados": {"junos_os": ["<22.4R1"]},
            "acción_recomendada": "Update Junos OS to correct version.",
            "puntuacion_cvss": "7.8",
            "tipo_vulnerabilidad": "Privilege Escalation",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "F5 BIG-IP TMUI remote command execution vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-F5-BIGIP",
        "rawcontent": "An unauthenticated remote command execution vulnerability has been reported in F5 BIG-IP Traffic Management User Interface.",
        "tags": {
            "cve_id": "CVE-2024-F5-BIGIP",
            "severidad": "Crítico",
            "activos_afectados": {"f5_bigip": ["<16.1.4"]},
            "acción_recomendada": "Apply BIG-IP security hotfix.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Log4j 2.15.0 security advisory details Log4Shell mitigation bypasses",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45046",
        "rawcontent": "A vulnerability in Log4j 2.15.0 allows remote attackers to cause Denial of Service or execute arbitrary code under non-default configurations.",
        "tags": {
            "cve_id": "CVE-2021-45046",
            "severidad": "Crítico",
            "activos_afectados": {"log4j": ["==2.15.0"]},
            "acción_recomendada": "Upgrade Log4j to version 2.16.0 or higher.",
            "puntuacion_cvss": "9.0",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Spring Framework remote code execution via class loader manipulation",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22965",
        "rawcontent": "A vulnerability in Spring Framework running on JDK 9+ allows remote attackers to obtain RCE via class loader parameter manipulation.",
        "tags": {
            "cve_id": "CVE-2022-22965",
            "severidad": "Crítico",
            "activos_afectados": {"spring_framework": ["<5.3.18"]},
            "acción_recomendada": "Update Spring Framework to 5.3.18 or higher.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Ruby on Rails security update addresses cross-site scripting",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-RAILS-XSS",
        "rawcontent": "A cross-site scripting vulnerability in Ruby on Rails template helpers allows injecting scripts via user-supplied model names.",
        "tags": {
            "cve_id": "CVE-2024-RAILS-XSS",
            "severidad": "Medio",
            "activos_afectados": {"rails": ["<7.0.8"]},
            "acción_recomendada": "Update Rails framework.",
            "puntuacion_cvss": "6.1",
            "tipo_vulnerabilidad": "XSS",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Django framework SQL injection in JSONField filter",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-DJANGO-SQLI",
        "rawcontent": "Django versions containing JSONField features are vulnerable to SQL injection when filtering JSON values via specific operators.",
        "tags": {
            "cve_id": "CVE-2024-DJANGO-SQLI",
            "severidad": "Alto",
            "activos_afectados": {"django": ["<4.2.8"]},
            "acción_recomendada": "Update Django configuration.",
            "puntuacion_cvss": "8.1",
            "tipo_vulnerabilidad": "SQL Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Laravel framework SQL injection in query builder",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-LARAVEL-SQLI",
        "rawcontent": "A vulnerability in Laravel framework query builder allows SQL injection when processing order clauses using raw user data.",
        "tags": {
            "cve_id": "CVE-2024-LARAVEL-SQLI",
            "severidad": "Alto",
            "activos_afectados": {"laravel": ["<10.3.3"]},
            "acción_recomendada": "Upgrade Laravel framework.",
            "puntuacion_cvss": "8.1",
            "tipo_vulnerabilidad": "SQL Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Grafana dashboard remote file disclosure vulnerability",
        "url": "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-GRAFANA-DISCL",
        "rawcontent": "A path traversal vulnerability in Grafana allows unauthenticated users to read arbitrary local files from the server hosting dashboard.",
        "tags": {
            "cve_id": "CVE-2024-GRAFANA-DISCL",
            "severidad": "Alto",
            "activos_afectados": {"grafana": ["<=8.3.3"]},
            "acción_recomendada": "Upgrade Grafana immediately.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Path Traversal",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    }
]

async def inyectar_mock_news():
    dsn = os.getenv("dsn")
    if not dsn:
        print("Error: No se encontró la variable 'dsn' en el archivo .env")
        return
        
    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(dsn)
    
    print(f"Inyectando {len(mock_news)} noticias de prueba pre-procesadas...")
    
    exito = 0
    errores = 0
    
    for news in mock_news:
        try:
            tags_json = json.dumps(news["tags"])
            
            await conn.execute("""
                INSERT INTO noticias (title, url, rawcontent, processed, tags, extractdate, processdate)
                VALUES ($1, $2, $3, TRUE, $4, NOW(), NOW())
                ON CONFLICT (url) DO NOTHING
            """, news["title"], news["url"], news["rawcontent"], tags_json)
            exito += 1
        except Exception as e:
            print(f"Error inyectando noticia '{news['title']}': {e}")
            errores += 1

    print(f"\nProceso finalizado. {exito} noticias inyectadas con éxito (o ya existían), {errores} errores.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(inyectar_mock_news())
