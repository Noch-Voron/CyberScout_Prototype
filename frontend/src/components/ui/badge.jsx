import * as React from "react";

function Badge({ variant = "default", className = "", children, ...props }) {
  const base = "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold";
  const variants = {
    default: "bg-blue-600 text-gray-800",
    secondary: "bg-gray-200 text-gray-800",
    destructive: "bg-red-600 text-white",
    outline: "border border-gray-400 text-gray-800",
  };
  return (
    <span
      className={`${base} ${variants[variant] || variants.default} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}

export { Badge };
