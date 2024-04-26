import torch
from transformers import BertTokenizer, BertModel
from transformers import BartForConditionalGeneration, BartTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter
import joblib
import pickle

class KubesenseGenerator:
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()

    def generate_embedding(self, user_input):
        tokenized_input = self.tokenizer.encode(user_input, add_special_tokens=True, max_length=128, truncation=True)
        input_tensor = torch.tensor(tokenized_input).to(self.device)
        input_tensor = input_tensor.unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(input_tensor)
        last_hidden_state = outputs.last_hidden_state
        embedding = last_hidden_state[:, 0, :]
        return embedding

    def calculate_similarity(self, target_embedding, dataset_embeddings):
        # Convert target embedding and dataset embeddings to numpy arrays
        target_embedding_np = target_embedding.cpu().numpy()
        dataset_embeddings_np = dataset_embeddings.cpu().numpy()

        # Calculate cosine similarity between the target embedding and each embedding in the dataset
        similarities = cosine_similarity(target_embedding_np, dataset_embeddings_np)
        return similarities.squeeze()

    def get_closest_matches(self, similarities, data, command_type, k=10):
        # Rank dataset examples based on similarity
        ranked_indices = np.argsort(similarities)[::-1]

        # Get the top-k closest matches
        closest_matches_indices = ranked_indices[:k]

        filtered_user_prompts = [prompt for prompt, prompt_type in zip(data['command'], data['type']) if prompt_type == command_type]

        # Extract the corresponding kubectl commands
        closest_matches_commands = [filtered_user_prompts[i] for i in closest_matches_indices]

        return closest_matches_commands

    def get_most_occurring_command(self, commands):
        # occurrences of each command
        command_counts = Counter(commands)

        # most common command and its count
        most_common_command, count = command_counts.most_common(1)[0]

        return most_common_command

    def load_and_classify_command(self, prompt):
        # Load the saved model
        with open('svm_model/svm_classifier_model.pkl', 'rb') as f:
            svm_classifier = pickle.load(f)
        with open('svm_model/tfidf_vectorizer.pkl', 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        with open('svm_model/label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)

        # Preprocess the prompt
        prompt_tfidf = tfidf_vectorizer.transform([prompt])

        # Make predictions
        predicted_label = svm_classifier.predict(prompt_tfidf)
        predicted_type = label_encoder.inverse_transform(predicted_label)

        return predicted_type

    def custom_generate_kubectl(self, data, prompt):
        print('-----------Kubesense-----------')
        print('   ')
        command_type = self.load_and_classify_command(prompt)
        print("Command type: ", command_type)

        filtered_user_inputs = [prompt for prompt, prompt_type in zip(data['prompt'], data['type']) if
                                prompt_type == command_type]

        # Initialize a list to store the embeddings
        embeddings = []

        # Loop through each user input
        for user_input in filtered_user_inputs:
            embedding = self.generate_embedding(user_input)

            # Append the embedding to the list of embeddings
            embeddings.append(embedding)

        # Concatenate the embeddings along the batch dimension
        embeddings_tensor = torch.cat(embeddings, dim=0)

        target_embedding = self.generate_embedding(prompt)

        # Calculate similarity with each embedding in the dataset
        similarities = self.calculate_similarity(target_embedding, embeddings_tensor)

        closest_matches_commands = self.get_closest_matches(similarities, data, command_type)

        most_occurring_command = self.get_most_occurring_command(closest_matches_commands)

        print(' ')
        print('Generated kubectl command: ', most_occurring_command)
        return most_occurring_command


    def bart_generate_kubectl(self, prompt):
        # Load fine-tuned BART model
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')
        model.load_state_dict(torch.load('llm_bart_model/fine_tuned_bart_model.pth', map_location=torch.device('cpu')))
        model.eval()

        # Load tokenizer using pickle
        # with open('llm_bart_model/tokenizer.pkl', 'rb') as f:
        #     tokenizer = pickle.load(f)

        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')

        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        generated_ids = model.generate(input_ids=input_ids, max_length=50, num_beams=4, early_stopping=True)
        generated_command = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        generated_command = generated_command.replace("(", "").replace(")", "")

        print(f'User Prompt: {prompt}')
        print(f'Generated kubectl Command: {generated_command}')

        return generated_command

    def custom_ensemble(self, user_input, model1_pred, model2_pred):

        resource_types = ['pod', 'svc', 'statefulset', 'secret', 'namespaces']

        if model1_pred == model2_pred:
            print('[INFO] Both models have identical predictions')
            return model1_pred
        else:
            for res in resource_types:
                if res in user_input:
                    if res in model1_pred:
                        print(
                            '[INFO] The ensemble prediction has been successfully generated based on the combined outputs of multiple models. This decision reflects the culmination of the predictive capabilities of the constituent models, ensuring a robust and informed course of action')
                        return model1_pred
                    elif res in model2_pred:
                        print(
                            '[INFO] The ensemble prediction has been successfully generated based on the combined outputs of multiple models. This decision reflects the culmination of the predictive capabilities of the constituent models, ensuring a robust and informed course of action')
                        return model2_pred

    def entity_replacing(self, prompt, generated_command_template):
        # Extract resource name and namespace from the prompt

        if "resource:" in prompt and "namespace:" in prompt:
            print("both")
            resource_name = prompt.lower().split("resource:")[1].strip().split(" ")[0]
            # namespace = prompt.split("namespace:")[1].split(" ")[0]
            namespace = prompt.lower().split("namespace:")[1].strip().split(" ")[0]

            formatted_command = generated_command_template.replace("<name>", resource_name, 1).replace("<name>",
                                                                                                       namespace, 1)
            return formatted_command
        elif "namespace:" in prompt and "resource:" not in prompt:
            "only ns"
            namespace = prompt.lower().split("namespace:")[1].strip().split(" ")[0]
            formatted_command = generated_command_template.replace("<name>", namespace)
            return formatted_command
        else:
            "none"
            print("[INFO] No resources or namespaces specified in the prompt")
            return generated_command_template

    # # main generating command function
    # def generate(self):
    #     return None
    #
    # # main executing in cluster function
    # def execute_in_GCP_cluster(self):
    #     return None


