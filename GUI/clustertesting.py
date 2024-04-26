# import subprocess
#
# def execute_command(command):
#     try:
#         # Execute the command in a shell and capture the output
#         result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#         # Decode the stdout and stderr bytes to strings
#         output_stdout = result.stdout.decode('utf-8')
#         output_stderr = result.stderr.decode('utf-8')
#
#         combined = output_stdout + "\n" + output_stderr
#
#         return combined
#     except subprocess.CalledProcessError as e:
#         return f"Error: {e}"
#
# def main():
#     # Activate the virtual environment and then run subsequent commands within the same process
#     kube = "kubectl get pods"
#     command = (f"call C:/Users/acer/PycharmProjects/CustomTkinter-master/Scripts/activate.bat && gcloud container clusters get-credentials cluster-fyp --zone us-central1-c --project kubesense && {kube}")
#     combined = execute_command(command)
#
#     print('Result', combined)
#
# if __name__ == "__main__":
#     main()



from Kubesense.GUI.DatasetCreator import DatasetCreator
from Kubesense.GUI.MultiModelCommandGenerator import KubesenseGenerator
from Kubesense.GUI.driver import KubeDriver

file_path = 'C:/Users/acer/Desktop/(DS and AI) Lectures/4th Year/CM4605-Individual Research Project/kubesense/Kubesense-FYP/Kubesense/Dataset/updted_data_with_class.json'
creator = DatasetCreator(json_path=file_path, csv_path='data.csv')
data = creator.create_dataset()

kubesense_generator = KubesenseGenerator()
driver = KubeDriver(data, kubesense_generator)

user_input = "Can I view the namespaces available in the cluster"
# output = driver.generate(user_input)
# print("[SUCCESS] Output: ", output)


output_from_cluster = driver.generate_and_execute(user_input)
print("Output from cluster: ", output_from_cluster)


# user_input = "i want to get the namespaces available"
# a = "kubectl get namespaces"
# b = "kubectl get namespaces"
# x = kubesense_generator.custom_ensemble(user_input, a, b)
# print(x)