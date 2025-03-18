 # Requirements

 - Kubernetes documentation [repository](https://github.com/kubernetes/website) should be available in the local machine 
 - Docker

## Building the image
```
cd k8s_vector_store_manager
docker build -t langchain-vdb .
```

## Generate embedings
```
docker run --volume /tmp/testcontainer:/tmp/testcontainer --volume <your-local-path-to-k8s-doc-repo>:/tmp/website -e GENERATE_EMBEDINGS=True langchain-vdb
```

## Retrieval of Documents

```
docker run --volume /tmp/testcontainer:/tmp/testcontainer --volume <your-local-path-to-k8s-doc-repo>:/tmp/website -e QUERY="what is a deployment?" langchain-vdb
```


