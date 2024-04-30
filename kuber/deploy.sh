docker build --platform=linux/amd64 -t ashmitkx/rc-proj:latest .
docker push ashmitkx/rc-proj:latest

kubectl apply -f deployment.yml
kubectl rollout restart deployment 
