# KMS Petshop Backend - Vercel Deployment Guide

## 🚀 Deployment Steps

### 1. Prerequisites
- Vercel account (https://vercel.com)
- MongoDB Atlas account (https://www.mongodb.com/atlas)
- Git repository

### 2. Environment Variables Setup
Set these environment variables in Vercel dashboard:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
JWT_SECRET=your-super-secret-jwt-key-here  
JWT_EXPIRES_MIN=60
ENVIRONMENT=production
```

### 3. MongoDB Atlas Setup
1. Create MongoDB Atlas cluster
2. Create database user with read/write permissions
3. Whitelist Vercel IP addresses (or use 0.0.0.0/0 for all IPs)
4. Copy connection string and add to MONGO_URI

### 4. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
npm i -g vercel
vercel login
vercel --prod
```

#### Option B: Using Vercel Dashboard
1. Connect your GitHub repository
2. Import project to Vercel
3. Add environment variables
4. Deploy

### 5. Verify Deployment
After deployment, test these endpoints:
- `GET /` - API information
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

## 📡 API Endpoints

### Base URL
```
https://your-app-name.vercel.app
```

### Available Endpoints
- **Auth**: `/api/auth/*`
- **Users**: `/api/user/*`
- **Layanan**: `/api/layanan/*`
- **Kucing**: `/api/kucing/*`
- **Keranjang**: `/api/keranjang/*`
- **Pesanan**: `/api/pesanan/*`
- **Pembayaran**: `/api/pembayaran/*`
- **Admin**: `/api/admin/*`
- **Knowledge**: `/api/knowledge/*`

## 🔧 Configuration Files

- `vercel.json` - Vercel deployment configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `.env.example` - Environment variables template
- `.vercelignore` - Files to ignore during deployment

## 🛠️ Troubleshooting

### Common Issues
1. **Module import errors**: Ensure all dependencies are in requirements.txt
2. **Database connection**: Check MongoDB Atlas whitelist and credentials
3. **Environment variables**: Verify all required vars are set in Vercel
4. **Cold start**: First request may be slow due to serverless cold start

### Monitoring
- Use Vercel dashboard for deployment logs
- Monitor function execution times
- Check error rates and performance metrics

## 🔒 Security Considerations
- Use strong JWT secret
- Implement rate limiting for production
- Regularly rotate secrets
- Monitor API usage patterns
