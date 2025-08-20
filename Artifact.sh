PROJECT_ID="pure-girder-452812-r3"
REPO="microservices"
REGION="asia-south1"

docker tag microservices_users $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/users:latest
docker tag microservices_orders $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/orders:latest
docker tag microservices_gateway $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/gateway:latest


docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/users:latest
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/orders:latest
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/gateway:latest