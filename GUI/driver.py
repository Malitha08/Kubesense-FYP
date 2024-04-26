import subprocess

class KubeDriver:
    def __init__(self, data, kubesense_generator):
        self.data = data
        self.kubesense_generator = kubesense_generator

    def generate(self, user_input):
        print('[INFO] Start custom multi model approach')
        custom_mm_result = self.kubesense_generator.custom_generate_kubectl(self.data, user_input)
        print("[INFO] custom mm result: ", custom_mm_result)

        print('[INFO] Start LLM approach')
        llm_result = self.kubesense_generator.bart_generate_kubectl(user_input)
        print("[INFO] llm result: ", llm_result)

        print('[INFO] Start ensembling of 2 results')
        ensembled_command = self.kubesense_generator.custom_ensemble(user_input, custom_mm_result, llm_result)
        print("[SUCCESS] Generated kubectl command template: ", ensembled_command)

        print('[INFO] Replacing entities..')
        kubectl_output = self.kubesense_generator.entity_replacing(user_input, ensembled_command)
        print("[SUCCESS] Final Output: ", kubectl_output)

        return kubectl_output

    def generate_and_execute(self, user_input):
        kubectl_command = self.generate(user_input)
        try:
            # Execute the command in a shell and capture the output
            result = subprocess.run(kubectl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Decode the stdout and stderr bytes to strings
            output_stdout = result.stdout.decode('utf-8')
            output_stderr = result.stderr.decode('utf-8')

            combined_output = output_stdout + "\n" + output_stderr

            return combined_output
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

from Kubesense.GUI.DatasetCreator import DatasetCreator
from Kubesense.GUI.MultiModelCommandGenerator import KubesenseGenerator

file_path = 'C:/Users/acer/Desktop/(DS and AI) Lectures/4th Year/CM4605-Individual Research Project/kubesense/Kubesense-FYP/Kubesense/Dataset/updted_data_with_class.json'
creator = DatasetCreator(json_path=file_path, csv_path='data.csv')
data = creator.create_dataset()