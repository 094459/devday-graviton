### Running your multi-arch container on Amazon EKS

This is a set of instructions that you can use to demonstrate how you have run your multi-arch container in a multi-arch managed node group. Change the details based on how you have created your demo containers if following from the code examples.

> One thing I ran into was that I ran out of diskspace on my Cloud9 development environment. If you run out of space available, removing not needed local Docker images from the previous demos and then use: sudo docker system prune was the way I was able to free up space.

Install the tools - these should already be installed if you are using the cdk installed image.

```
> $ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_arm64.tar.gz" | tar xz -C /tmp
> $ sudo mv /tmp/eksctl /usr/local/bin
> $ curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.12/2020-11-02/bin/linux/arm64/kubectl
> $ chmod +x ./kubectl
> $ mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
```

You can now use the container built in the following example.

```
$ eksctl create cluster --name eks-multi-arch \
  --version 1.18 \
  --without-nodegroup
```

<takes a while to build the eks node>
  
```
$ kubectl get svc
```

if you get the error - "to create an ARM nodegroup kube-proxy, coredns and aws-node addons should be up to date. Please use `eksctl utils update-coredns`, `eksctl utils update-kube-proxy` and `eksctl utils update-aws-node` before proceeding."

```
$ eksctl utils update-kube-proxy --cluster=eks-multi-arch --approve
$ eksctl utils update-coredns --cluster=eks-multi-arch --approve
$ eksctl utils update-aws-node --cluster=eks-multi-arch --approve
```

```
eksctl create nodegroup \
  --cluster eks-multi-arch \
  --region eu-west-1 \
  --name x86-mng \
  --node-type m5.large \
  --nodes 1\
  --nodes-min 1\
  --nodes-max 2\
  --managed
```

```
 eksctl create nodegroup \
  --cluster eks-multi-arch \
  --region eu-west-1 \
  --name graviton-mng \
  --node-type m6g.large \
  --nodes 1\
  --nodes-min 1\
  --nodes-max 2\
  --managed
```

```  
$ kubectl get nodes --label-columns=kubernetes.io/arch
```

Edit the hello-world.yaml file for your environment

```
$ kubectl apply -f hello-world.yaml
```

```
$ kubectl get pod -o wide
```

It will start running the containers, to see the ouput - change replicas from 0 to 2 and then back again

```
$ kubectl logs {pod from prev. command}
```

To clean up, make sure you remove all the resources created.

```
eksctl delete nodegroup --name graviton-mng --cluster eks-multi-arch
eksctl delete nodegroup --name x86-mng --cluster eks-multi-arch
eksctl delete cluster --name eks-multi-arch
```
 