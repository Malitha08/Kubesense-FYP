# from transformers import BertTokenizer, BertModel
# from transformers import RobertaTokenizer, RobertaModel
# import torch
from GUI.DatasetCreator import DatasetCreator
from GUI.MultiModelCommandGenerator import KubesenseGenerator


file_path = 'C:/Users/acer/Desktop/(DS and AI) Lectures/4th Year/CM4605-Individual Research Project/kubesense/Kubesense-FYP/Kubesense/Dataset/updted_data_with_class.json'
creator = DatasetCreator(json_path=file_path, csv_path='data.csv')
data = creator.create_dataset()


# Create an instance of EmbeddingGenerator
kubesense_generator = KubesenseGenerator()
# Generate embedding for user input
# user_input = "I want to delete the svc resource:svc1 in the namespace:x"
user_input = "I want to delete the pod resource:ser in the namespace:x"
# embedding = kubesense_generator.generate_embedding(user_input)
# # Do something with the embedding
# print(embedding)
#
#
# similarity = kubesense_generator.calculate_similarity(embedding, embedding)
# print("Similiarity: ", similarity)
#
# # similarities = [0.6, 0.5, 0.7, 0.3, 0.2, 0.4]
# # closest_matches = embedding_generator.get_closest_matches(similarities, data, k=6)
# # print(closest_matches)
#
# # commands = ['k get pods', 'k get svc', 'k get pods']
# # most_occ_commands = embedding_generator.get_most_occurring_command(commands)
# # print(most_occ_commands)
#
#
# command_type = kubesense_generator.load_and_classify_command(prompt=user_input)
# print('Command type: ', command_type)

# print('[INFO] Start custom multi model approach')
#
# custom_mm_result = kubesense_generator.custom_generate_kubectl(data, user_input)
# print("[INFO] custom mm result: ", custom_mm_result)
#
# print('[INFO] Start LLM approach')
# llm_result = kubesense_generator.bart_generate_kubectl(user_input)
# print("[INFO] llm result: ", llm_result)
#
# print('[INFO] Start ensembling of 2 results')
# ensembled_command = kubesense_generator.custom_ensemble(user_input, custom_mm_result, llm_result)
# print("[SUCCESS] Generated kubectl command templated: ", ensembled_command)
#
# print('[INFO] Replacing entities..')
# final_output = kubesense_generator.entity_replacing(user_input,ensembled_command)
# print("[SUCCESS] Final Output: ", final_output)

import tkinter as tk
from tkinter import ttk
from tkinter import font

class App:
    def __init__(self, master):
        self.master = master
        self.loading_icon = None

        # Create a Text widget
        self.output_textbox = tk.Text(master, height=5, width=40, bg="Grey", highlightthickness=2)
        self.output_textbox.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # Create a Run button
        self.run_button = tk.Button(master, text="Run", command=self.run_process)
        self.run_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def run_process(self):
        # Display loading icon
        self.loading_icon = ttk.Progressbar(self.master, mode="indeterminate")
        self.loading_icon.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.loading_icon.start()

        # Simulate a long-running process
        self.master.after(3000, self.process_complete)

    def process_complete(self):
        # Stop and remove the loading icon
        if self.loading_icon:
            self.loading_icon.stop()
            self.loading_icon.grid_remove()

        # Display the result in the Text widget
        self.output_textbox.insert(tk.END, "Process completed!")

root = tk.Tk()
app = App(root)
root.mainloop()


