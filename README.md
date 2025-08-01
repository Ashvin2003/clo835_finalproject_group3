# CLO835 Final - Group 3 - Enhanced Flask App with S3 Background Images

This project is an enhanced Flask web application with MySQL database that supports background images from S3, Kubernetes deployment with IRSA, and CI/CD pipeline.

## 🚀 Enhanced Features

- **Background Images from S3**: Application retrieves background images from private S3 bucket
- **ConfigMap Integration**: Background image URL, user name, aws access keys  provided via ConfigMap
- **Kubernetes Secrets**: MySQL credentials stored securely as Kubernetes secrets
- **IRSA Support**: Service account with IAM roles
- **Port 81**: Application listens on port 81 as requested
- **Comprehensive Logging**: Background image URL and application events logged
- **Modern UI**: Responsive design with background images instead of solid colors
- **CI/CD Pipeline**: GitHub Actions for automated testing and ECR deployment

## 🏗️ Project Structure

```
├── app.py                          # Enhanced Flask application
├── requirements.txt                 # Python dependencies
├── Dockerfile                      # Container configuration
├── templates/                      # HTML templates with background images
├── k8s/                           # Kubernetes manifests
│   ├── namespace.yaml             # Final namespace
│   ├── configmap.yaml            # App configuration
│   ├── secret.yaml               # Database credentials
│   ├── pvc.yaml                  # Persistent volume claim
│   ├── serviceaccount.yaml       # IRSA service account
│   ├── role.yaml                 # RBAC roles
│   ├── db/                       # Database manifests
│   │   ├── deployment.yaml      # MySQL deployment
│   │   ├── service.yaml         # MySQL service
│   │   └── init-configmap.yaml  # Database initialization
│   └── app/                      # Application manifests
│       ├── deployment.yaml       # Flask app deployment
│       └── service.yaml         # LoadBalancer service
├── .github/workflows/             # CI/CD pipeline
    └── ci-cd.yml                # GitHub Actions workflow

```

## 🐳 Local Development

### 1. Build Docker Images

```bash
# Build application image
docker build -t clo835-app .

# Build database image
docker build -t clo835-db -f db/Dockerfile .
```

### 2. Test Locally

```bash
# Create network
docker network create clo835-network

# Run MySQL database
docker run -d -p 3306:3306 \
  --network=clo835-network \
  -e MYSQL_ROOT_PASSWORD=password123 \
  --name=clo835-db clo835-db

# Run Flask application
docker run -d -p 8081:81 \
  --network=clo835-network \
  -e DBHOST=clo835-db \
  -e DBPORT=3306 \
  -e DBUSER=root \
  -e DBPWD=password123 \
  -e DATABASE=employees \
  -e BACKGROUND_IMAGE_URL=s3://your-bucket/background.jpg \
  -e USER_NAME="Senindu Mendis" \
  -e AWS_REGION=us-east-1 \
  --name=clo835-app clo835-app
```

## ☁️ AWS Setup

### 1. Create S3 Bucket

```bash
aws s3 mb s3://your-private-bucket
aws s3 cp background.jpg s3://your-private-bucket/
```

### 2. Create ECR Repository

```bash
aws ecr create-repository --repository-name clo835-app
```

### 3. Create IAM Role for IRSA

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-private-bucket",
                "arn:aws:s3:::your-private-bucket/*"
            ]
        }
    ]
}
```

### 4. Create EKS Cluster

```bash
eksctl create cluster \
  --name clo835-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 4 \
  --managed
```

## 🚀 Kubernetes Deployment

### 1. Create Namespace and Resources

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/role.yaml
```

### 2. Deploy Database

```bash
kubectl apply -f k8s/db/init-configmap.yaml
kubectl apply -f k8s/db/deployment.yaml
kubectl apply -f k8s/db/service.yaml
```

### 3. Deploy Application

```bash
kubectl apply -f k8s/app/deployment.yaml
kubectl apply -f k8s/app/service.yaml
```

### 4. Verify Deployment

```bash
kubectl get all -n final
kubectl get svc flask-app-service -n final
```

## 🔄 CI/CD Pipeline

### 1. GitHub Repository Setup

1. Push code to GitHub repository
2. Add AWS credentials as GitHub secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### 2. Automated Pipeline

The GitHub Actions workflow will:
1. Run unit tests
2. Build Docker image
3. Push to Amazon ECR
4. Deploy to Kubernetes (optional)

## 🔧 Configuration

### Environment Variables

- `BACKGROUND_IMAGE_URL`: S3 URL for background image
- `USER_NAME`: User name displayed in header
- `AWS_REGION`: AWS region for S3 access
- `DBHOST`: MySQL host
- `DBPORT`: MySQL port
- `DBUSER`: MySQL username
- `DBPWD`: MySQL password
- `DATABASE`: Database name

### ConfigMap Configuration

Update `k8s/configmap.yaml` with your S3 bucket details:

```yaml
data:
  BACKGROUND_IMAGE_URL: "s3://your-private-bucket/background.jpg"
  USER_NAME: "Senindu Mendis"
  AWS_REGION: "us-east-1"
```

## 📝 Logging

The application logs:
- Background image URL on startup
- User name and database configuration
- Employee operations (add/retrieve)
- S3 download operations
- Error messages

## 🔒 Security Features

- MySQL credentials stored in Kubernetes secrets
- S3 access via IRSA (IAM Roles for Service Accounts)
- Input validation and error handling
- Secure environment variable management

## 🧪 Testing

Run tests locally:

```bash
pip install pytest
python -m pytest tests/ -v
```

## 📊 Monitoring

Check application logs:

```bash
kubectl logs -f deployment/flask-app-deployment -n final
```

## 🎯 Key Features Implemented

✅ Background images from S3 instead of solid colors  
✅ ConfigMap for background image URL and user name  
✅ S3 image download and local storage  
✅ Comprehensive logging with background image URL  
✅ MySQL credentials via Kubernetes secrets  
✅ User name in HTML header via environment variable  
✅ Application listening on port 81  
✅ Docker image with local testing  
✅ GitHub Actions CI/CD pipeline  
✅ EKS cluster with 2 worker nodes  
✅ "final" namespace  
✅ ConfigMap for application configuration  
✅ Secret for database credentials  
✅ 2Gi PVC with gp2 storage class  
✅ Service account with IRSA permissions  
✅ RBAC roles and bindings  
✅ MySQL deployment with PVC  
✅ LoadBalancer service for external access  

## 👨‍💻 Developers

**Group 3**  
CLO835 Final - Enhanced Flask Application

Senindu Mendis
Ashvin Ravi
Jasleen Dhir
