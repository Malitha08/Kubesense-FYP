# Kubesense-FYP
Kubesense: A Cognitive Framework for revolutionizing kubernetes management 

Kubernetes, being a container orchestration and management system has been gaining popularity as the sector standard owing to the many appealing features, scalability, and an active ecosystem. Kubernetes is one of the first open-source projects of the Google company and its main aim is to supply a platform-agnostic solution ideal for the automatic deployment, scaling up, and management of containerized applications in a consistent manner. Effective administration of Kubernetes clusters is a challenge that needs to be overcome because of the complexity of the supporting infrastructure and the distinct operations needed for proper cluster administration. In order for an individual to operate on a Kubernetes cluster, an adequate level of experience of working with kubectl is required. 
In this thesis, the author proposes a novel approach to Kubernetes cluster management leveraging natural language understanding (NLU) techniques.  Kubesense, a Kubernetes management tool capable of interpreting user queries in plain natural language and generating corresponding kubectl commands and executing and performing cluster operations is introduced. The tool comprises of a large language model (LLM) for natural language processing tasks coupled with a novel multi-model approach, enabling seamless interaction with the cluster via the Kubernetes API through natural language human prompts.

# Pre-Resquisites
```
[Python 3.7] required
pip install -r requirements.txt
```

# Cloning and Setting Up the framework
```
git clone https://github.com/Malitha08/Kubesense-FYP.git
fetch the gcloud auth login to the desired K8s Cluster example: gcloud container clusters get-credentials [clusterName] --zone us-central1-c --project [projectName]
Insert this gcloud auth login to the login function in newui.py
Run the auth login command in your terminal
fine-tuned model directory link: https://drive.google.com/file/d/1468HEgexg9fpkJbbnGrzGmnXyoxcMaQr/view?usp=sharing
Download the fine_tuned_bart_model.pth file and insert it into llm_bart_model directory
cd GUI
Run newui.py -> python newui.py
```

# Achitecture
![image](https://github.com/Malitha08/Kubesense-FYP/assets/72942686/44d6806a-ae47-4c74-a7e7-bcac79dc72f4)

# Kubesense Usage
- Authenticate to cluster using gcloud auth login
- Enter the operation which needs to be performed
    - [IMPORTANT] When specifying resources and namespaces in the commands follow the approach:
    - Example prompt: "i want to edit the svc resource:svc_name in the namespace:ns"
    - Make sure that the resource name is preceeded by "resource:.." and the namespace is preceeded by "namespace:.."
- Execute Command -> Will generate and execute the kubectl command in the cluster and relay response to the GUI.
- Generate Command -> Will generate the kubectl command and relay response to GUI

# Data-Flow Diagram
![image](https://github.com/Malitha08/Kubesense-FYP/assets/72942686/66cf03f4-e573-4cb3-9605-02751ee02c0f)

