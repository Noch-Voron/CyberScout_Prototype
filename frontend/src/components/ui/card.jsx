import * as React from "react";

function Card({ className = "", children, ...props }) {
  return (
    <div
      className={`rounded-xl border bg-white shadow ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

function CardHeader({ className = "", children, ...props }) {
  return (
    <div className={`p-4 border-b ${className}`} {...props}>
      {children}
    </div>
  );
}

function CardTitle({ className = "", children, ...props }) {
  return (
    <h3 className={`font-semibold text-lg ${className}`} {...props}>
      {children}
    </h3>
  );
}

function CardContent({ className = "", children, ...props }) {
  return (
    <div className={`p-4 ${className}`} {...props}>
      {children}
    </div>
  );
}

function CardFooter({ className = "", children, ...props }) {
  return (
    <div className={`p-4 border-t flex justify-end ${className}`} {...props}>
      {children}
    </div>
  );
}

export { Card, CardHeader, CardTitle, CardContent, CardFooter };
