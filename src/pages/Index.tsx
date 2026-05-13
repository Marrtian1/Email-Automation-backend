import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Server, Code2, Database, Mail, ShieldCheck, Calendar } from "lucide-react";

const Index = () => {
  const features = [
    { icon: <Server className="w-5 h-5" />, title: "FastAPI Core", description: "Scalable structure with main.py entry point and modular routing." },
    { icon: <Database className="w-5 h-5" />, title: "PostgreSQL Ready", description: "SQLAlchemy models and database connection setup included." },
    { icon: <ShieldCheck className="w-5 h-5" />, title: "Security", description: "CORS middleware, Pydantic validation, and JWT preparation." },
    { icon: <Code2 className="w-5 h-5" />, title: "Modular Design", description: "Separated models, schemas, services, and API endpoints." },
    { icon: <Mail className="w-5 h-5" />, title: "Email Automation", description: "Pre-configured services for email handling and user management." },
    { icon: <Calendar className="w-5 h-5" />, title: "Scheduled Emails", description: "Automated delivery system with background processing and status tracking." },
  ];

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="text-center space-y-4">
          <Badge variant="outline" className="px-4 py-1 text-blue-600 border-blue-200 bg-blue-50">
            Backend Initialized
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
            Email Automation System
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            The FastAPI backend boilerplate has been successfully generated with a scalable folder structure and core configurations.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="border-none shadow-sm hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 mb-2">
                  {feature.icon}
                </div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>

        <Card className="border-blue-100 bg-blue-50/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle2 className="text-green-500" />
              Project Structure Created
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm font-mono">
              <div className="bg-white p-3 rounded border border-blue-100">app/api/</div>
              <div className="bg-white p-3 rounded border border-blue-100">app/models/</div>
              <div className="bg-white p-3 rounded border border-blue-100">app/schemas/</div>
              <div className="bg-white p-3 rounded border border-blue-100">app/services/</div>
              <div className="bg-white p-3 rounded border border-blue-100">app/core/</div>
              <div className="bg-white p-3 rounded border border-blue-100">main.py</div>
              <div className="bg-white p-3 rounded border border-blue-100">requirements.txt</div>
              <div className="bg-white p-3 rounded border border-blue-100">.env</div>
            </div>
            
            <div className="mt-6 p-4 bg-slate-900 rounded-lg text-slate-300 font-mono text-sm">
              <p className="text-blue-400"># To run the backend locally:</p>
              <p>pip install -r requirements.txt</p>
              <p>uvicorn app.main:app --reload</p>
            </div>
          </CardContent>
        </Card>

        <footer className="text-center text-slate-500 text-sm">
          Ready for the next set of instructions.
        </footer>
      </div>
    </div>
  );
};

export default Index;
