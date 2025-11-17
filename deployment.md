```bash 

export REGION="asia-northeast1"

export PROJECT_ID="dev-projects-476011"

gcloud secrets create LINE_CHANNEL_ACCESS_TOKEN --replication-policy="automatic" --data-file=- <<< "xxx"

gcloud secrets create LINE_CHANNEL_SECRET --replication-policy="automatic" --data-file=- <<< "xx"

IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/line-poster/line-poster:latest"

gcloud artifacts repositories create line-poster \
  --repository-format=docker \
  --location=$REGION

docker build --platform linux/amd64 -t line-poster:local -f ./Dockerfile .

docker tag line-poster:local $IMAGE_NAME

docker push $IMAGE_NAME

# Note this is a job, not service
gcloud run jobs create line-poster-job \
  --image=$IMAGE_NAME \
  --region=$REGION \
  --task-timeout=15m \
  --set-secrets="\
LINE_CHANNEL_ACCESS_TOKEN=LINE_CHANNEL_ACCESS_TOKEN:latest,\
LINE_CHANNEL_SECRET=LINE_CHANNEL_SECRET:latest"
```