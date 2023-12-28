#image icon appears no matter what, seems like a graphical error...grrrrrrrrrrrrrrrrr

import webview
import os

def load_html(window):
    image_path = "C:\\Users\\nvbue\\Downloads\\corgi.jpg"
    if os.path.exists(image_path):
        image_tag = "<img src='file://"+image_path.replace('\\', '/').replace(' ', '%20')+"alt='Yarr'>"
        html_content = f"""
        <html>
            <body>
                {image_tag}
            </body>
        </html>
        """
        window.load_html(html_content)
    else:
        print(f"Image file not found at {image_path}")

if __name__ == "__main__":
    window = webview.create_window(title="Server Control")
    webview.start(load_html, window, http_server=True)







# import os

# import webview
# import base64

# class API:
#     # Function to process user input and return images or strings
#     def process_command(self,command):
#         # Your logic to process the command and generate response (image or string)
#         print(command+"!")
#         if command == "image":
#             with open('D:\\converted\\2021\\04\\03\\4.JPG', 'rb') as image_file:
#                 encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
#             return f'data:image/png;base64,{encoded_image}'
#         else:
#             print("cum")
#             return f"You entered: {command}. This is a text response."

#     # Callback function to handle user commands
#     def handle_command(self,command):
#         response = self.process_command(command)
#         return f"updateResponse('{response}')"

# # Creating the UI
# def create_ui():
#     html = """
#     <html>
#     <body>
#         <h1>Send Command</h1>
#         <input type="text" id="commandInput" placeholder="">
#         <button onclick="sendCommand()">Send</button>
#         <img src = response, alt="GRRRR"/>
#         <script>
#             function sendCommand() {
#                 var command = document.getElementById('commandInput').value;
#                 pywebview.api.handle_command(command).then(updateResponse);
#                 document.getElementById('commandInput').value=""
#             }
            
#             function updateResponse(response) {
#                 document.getElementById('response').innerHTML = response;
#             }
#         </script>
#     </body>
#     </html>
#     """
#     api=API()
#     webview.create_window("Command Sender", html=html, js_api=api)
#     webview.start(http_server=True)

# if __name__ == "__main__":
#     create_ui()
    
