from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
CORS(app,supports_credentials=True)


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

# assistant = client.beta.assistants.create(
#     name="Financial Analyst Assistant",
#     instructions="You are an expert financial analyst. Use your knowledge base to answer questions about audited financial statements.",
#     model="gpt-4o-mini",
#     tools=[{"type": "file_search"}],
# )

# vector_store = client.beta.vector_stores.create(name="Financial Statements")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('prompt')

    try:
        # Create a new thread for the assistant
        thread = client.beta.threads.create()

        # Send the user message to the assistant
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Create and poll the run to get the assistant's response
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id='asst_1tGTpItw2FrfxE7lvtgEX6HR',
            instructions="Please address the user."
        )

        # Check if the response is completed
        # if run.status == 'completed':
        #     messages_page = client.beta.threads.messages.list(thread_id=thread.id)
        #     messages = messages_page.data  # 使用 .data 來獲取消息列表
        #     latest_message = messages[-1]  # 獲取最新的消息
        #     print({'response': latest_message.content})
        #     return jsonify({'response': latest_message.content})  # 返回最新消息的內容
        # else:
        #     print({'error': 'Assistant response is not completed.'})
        #     return jsonify({'error': 'Assistant response is not completed.'})
        if run.status == 'completed':
            messages_page = client.beta.threads.messages.list(thread_id=thread.id)
            messages = messages_page.data  # 使用 .data 獲取消息列表
            latest_message = messages[-2]  # 獲取最新的消息

            # 提取文本內容
            content_blocks = latest_message.content
            response_text = ''
            for block in content_blocks:
                if hasattr(block, 'text') and hasattr(block.text, 'value'):
                    response_text += block.text.value + '\n'

            return jsonify({'response': response_text.strip()})  # 返回純文本
        else:
            return jsonify({'error': 'Assistant response is not completed.'})
    
    
    except Exception as e:
        print({'error': str(e)})
        return jsonify({'error': str(e)})

@app.route('/test', methods=['GET'])
def test():
    try:
        return "hello"
    except Exception as e:  # 'Exception' 和 'e' 是正确的变量名称
        print(str(e))
        return str(e) 

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'})

#     file = request.files['file']

#     if file.filename == '':
#         return jsonify({'error': 'No file selected'})
#     # 確認文件是 PDF
#     if not file.filename.lower().endswith('.pdf'):
#         return jsonify({'error': 'Only PDF files are allowed'})
    
#     try:
#          # 確保文件 MIME 類型是 application/pdf
#         if file.mimetype != 'application/pdf':
#             print({'error': 'Uploaded file is not a valid PDF'})
#             return jsonify({'error': 'Uploaded file is not a valid PDF'})

#         # 上傳文件到向量存儲
#         file_streams = [(file.filename, file.stream, 'application/pdf')]  # 明確指定文件名和 MIME 類型
#         #file_streams = [file.stream]

#         # Upload the file to the vector store
#         file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#             vector_store_id=vector_store.id,
#             files=file_streams
#         )

#         # Update assistant with the new file
#         client.beta.assistants.update(
#             assistant_id=assistant.id,
#             tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
#         )

#         return jsonify({'status': file_batch.status, 'file_counts': file_batch.file_counts})

#     except Exception as e:
#         print({'error': str(e)})
#         return jsonify({'error': str(e)})
    


@app.route('/uploads', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     user_input = data.get('prompt')

#     try:
#         # 呼叫 OpenAI API
        
#         response =client.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages=[
#                 {'role': 'user', 'content': user_input}
#             ],
#             max_tokens=900
#         )
#         response_content = response.choices[0].message.content
#         print(({'response': response_content}))
#         return jsonify({'response': response_content})

#     except Exception as e:
#         print({'error': str(e)})
#         return jsonify({'error': str(e)})


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)
