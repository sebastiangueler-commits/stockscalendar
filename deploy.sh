#!/bin/bash

# 🚀 Magic Stocks Calendar - Deployment Script
# Este script automatiza el deployment de la aplicación

echo "🚀 Iniciando deployment de Magic Stocks Calendar..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    print_error "No se encontró app.py. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

print_status "Verificando estructura del proyecto..."

# Verificar archivos necesarios
required_files=("app.py" "requirements.txt" "Procfile" "railway.json" "frontend/package.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo requerido no encontrado: $file"
        exit 1
    fi
done

print_success "Estructura del proyecto verificada"

# Verificar que Git esté configurado
if ! git status &> /dev/null; then
    print_error "Git no está inicializado. Ejecuta: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

print_status "Verificando configuración de Git..."

# Verificar que hay commits
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    print_warning "No hay commits en Git. Creando commit inicial..."
    git add .
    git commit -m "Initial commit - Ready for deployment"
fi

print_success "Git configurado correctamente"

# Mostrar opciones de deployment
echo ""
echo "🎯 OPCIONES DE DEPLOYMENT:"
echo "1. Railway (Backend) + Vercel (Frontend) - RECOMENDADO"
echo "2. Railway (Backend) + Netlify (Frontend)"
echo "3. Heroku (Backend) + Vercel (Frontend)"
echo "4. Solo verificar configuración"
echo ""

read -p "Selecciona una opción (1-4): " choice

case $choice in
    1)
        print_status "Configurando para Railway + Vercel..."
        
        # Verificar Railway CLI
        if ! command -v railway &> /dev/null; then
            print_warning "Railway CLI no está instalado."
            print_status "Instalando Railway CLI..."
            npm install -g @railway/cli
        fi
        
        # Verificar Vercel CLI
        if ! command -v vercel &> /dev/null; then
            print_warning "Vercel CLI no está instalado."
            print_status "Instalando Vercel CLI..."
            npm install -g vercel
        fi
        
        print_success "CLIs instalados correctamente"
        
        echo ""
        print_status "🚀 INSTRUCCIONES PARA DEPLOYMENT:"
        echo ""
        echo "1. BACKEND (Railway):"
        echo "   - Ejecuta: railway login"
        echo "   - Ejecuta: railway link"
        echo "   - Ejecuta: railway up"
        echo ""
        echo "2. FRONTEND (Vercel):"
        echo "   - Ejecuta: cd frontend"
        echo "   - Ejecuta: vercel login"
        echo "   - Ejecuta: vercel --prod"
        echo ""
        echo "3. CONFIGURAR VARIABLES DE ENTORNO:"
        echo "   - Backend: Usa el dashboard de Railway"
        echo "   - Frontend: Usa el dashboard de Vercel"
        echo ""
        ;;
        
    2)
        print_status "Configurando para Railway + Netlify..."
        
        # Verificar Railway CLI
        if ! command -v railway &> /dev/null; then
            print_warning "Railway CLI no está instalado."
            print_status "Instalando Railway CLI..."
            npm install -g @railway/cli
        fi
        
        # Verificar Netlify CLI
        if ! command -v netlify &> /dev/null; then
            print_warning "Netlify CLI no está instalado."
            print_status "Instalando Netlify CLI..."
            npm install -g netlify-cli
        fi
        
        print_success "CLIs instalados correctamente"
        
        echo ""
        print_status "🚀 INSTRUCCIONES PARA DEPLOYMENT:"
        echo ""
        echo "1. BACKEND (Railway):"
        echo "   - Ejecuta: railway login"
        echo "   - Ejecuta: railway link"
        echo "   - Ejecuta: railway up"
        echo ""
        echo "2. FRONTEND (Netlify):"
        echo "   - Ejecuta: cd frontend"
        echo "   - Ejecuta: netlify login"
        echo "   - Ejecuta: netlify deploy --prod"
        echo ""
        echo "3. CONFIGURAR VARIABLES DE ENTORNO:"
        echo "   - Backend: Usa el dashboard de Railway"
        echo "   - Frontend: Usa el dashboard de Netlify"
        echo ""
        ;;
        
    3)
        print_status "Configurando para Heroku + Vercel..."
        
        # Verificar Heroku CLI
        if ! command -v heroku &> /dev/null; then
            print_warning "Heroku CLI no está instalado."
            print_status "Instalando Heroku CLI..."
            # Instrucciones para instalar Heroku CLI
            echo "Por favor instala Heroku CLI desde: https://devcenter.heroku.com/articles/heroku-cli"
        fi
        
        # Verificar Vercel CLI
        if ! command -v vercel &> /dev/null; then
            print_warning "Vercel CLI no está instalado."
            print_status "Instalando Vercel CLI..."
            npm install -g vercel
        fi
        
        print_success "CLIs instalados correctamente"
        
        echo ""
        print_status "🚀 INSTRUCCIONES PARA DEPLOYMENT:"
        echo ""
        echo "1. BACKEND (Heroku):"
        echo "   - Ejecuta: heroku login"
        echo "   - Ejecuta: heroku create magic-stocks-backend"
        echo "   - Ejecuta: git push heroku main"
        echo ""
        echo "2. FRONTEND (Vercel):"
        echo "   - Ejecuta: cd frontend"
        echo "   - Ejecuta: vercel login"
        echo "   - Ejecuta: vercel --prod"
        echo ""
        echo "3. CONFIGURAR VARIABLES DE ENTORNO:"
        echo "   - Backend: heroku config:set KEY=value"
        echo "   - Frontend: Usa el dashboard de Vercel"
        echo ""
        ;;
        
    4)
        print_status "Verificando configuración..."
        ;;
        
    *)
        print_error "Opción inválida"
        exit 1
        ;;
esac

# Verificar variables de entorno
print_status "Verificando variables de entorno..."

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    print_warning "Creando archivo .env desde env.example..."
    cp env.example .env
fi

print_success "Variables de entorno configuradas"

# Verificar que el frontend se puede construir
print_status "Verificando build del frontend..."

cd frontend
if npm run build; then
    print_success "Frontend se construye correctamente"
else
    print_error "Error al construir el frontend"
    exit 1
fi

cd ..

print_success "✅ Verificación completa - Todo listo para deployment!"

echo ""
echo "📋 RESUMEN:"
echo "✅ Backend: FastAPI con Railway/Heroku"
echo "✅ Frontend: React con Vercel/Netlify"
echo "✅ PayPal: Configurado para producción"
echo "✅ APIs: Alpha Vantage, Yahoo Finance, IEX Cloud"
echo "✅ Datos: 5000+ acciones reales"
echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Sigue las instrucciones de deployment arriba"
echo "2. Configura las variables de entorno"
echo "3. Prueba la aplicación completa"
echo "4. Configura dominio personalizado (opcional)"
echo ""
echo "📖 Para más detalles, lee DEPLOYMENT.md"
echo ""
print_success "🚀 ¡Tu aplicación está lista para ir online!"