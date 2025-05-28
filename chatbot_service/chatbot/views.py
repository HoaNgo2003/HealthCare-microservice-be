from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv
from deep_translator import GoogleTranslator

import os
import warnings

warnings.filterwarnings("ignore")

# Load environment variables (HF_TOKEN, etc.)
load_dotenv(find_dotenv())


def translate_to_vietnamese(text):
    return GoogleTranslator(source="auto", target="vi").translate(text)


# Load LLM
HF_TOKEN = os.environ.get("HF_TOKEN")
print(f"HF_TOKEN={HF_TOKEN}")
HUGGINGFACE_REPO_ID = "HuggingFaceH4/zephyr-7b-beta"


def load_llm():
    return HuggingFaceEndpoint(
        repo_id=HUGGINGFACE_REPO_ID,
        temperature=0.5,
        max_new_tokens=512,
        huggingfacehub_api_token=HF_TOKEN,
    )


# Load Vector DB
DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db = FAISS.load_local(
    DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True
)

# Prompt Template
CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you don't know the answer, just say you don't know, don't try to make up an answer.
Don't provide anything out of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""


def set_custom_prompt():
    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"]
    )


# QA Chain (load once)
qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": set_custom_prompt()},
)


# === API View ===
class ChatbotVer1View(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_question = request.data.get("message", "").strip()

        if not user_question:
            return Response(
                {"error": "Missing 'message' field."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = qa_chain.invoke({"query": user_question})
            answer = result["result"]
            sources = [
                {"page_content": doc.page_content, "metadata": doc.metadata}
                for doc in result["source_documents"]
            ]

            vietnamese_answer = translate_to_vietnamese(answer)

            return Response({"reply": vietnamese_answer, "sources": sources})

        except Exception as e:
            return Response(
                {"error": "Failed to process query.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv, find_dotenv
import os


class BuildMemoryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Step 1: Load PDF from data/
            DATA_PATH = "data/"
            loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
            documents = loader.load()
            if not documents:
                return Response({"error": "No PDF files found in data/"}, status=404)

            # Step 2: Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=50
            )
            text_chunks = text_splitter.split_documents(documents)

            # Step 3: Embedding
            embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Step 4: Save to FAISS
            DB_FAISS_PATH = "vectorstore/db_faiss"
            os.makedirs("vectorstore", exist_ok=True)
            db = FAISS.from_documents(text_chunks, embedding_model)
            db.save_local(DB_FAISS_PATH)

            return Response({"message": "Vector store built successfully."}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from PIL import Image
from slugify import slugify
from io import BytesIO
import os
from urllib.parse import urljoin


class UnicodePDFWithImages(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
        self.set_font("DejaVu", "", 12)
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)

    def write_text(self, text):
        for line in text.split("\n"):
            self.multi_cell(0, 10, line)

    def write_image(self, image_url, base_url):
        try:
            # Nếu là link tương đối → chuyển sang tuyệt đối
            full_url = urljoin(base_url, image_url)

            img_response = requests.get(full_url, timeout=5)
            if img_response.status_code != 200:
                print(f"[!] Skip image: {full_url} (status {img_response.status_code})")
                return

            img = Image.open(BytesIO(img_response.content)).convert("RGB")
            temp_path = "temp_image.jpg"
            img.save(temp_path)

            self.ln(5)
            self.image(temp_path, w=min(self.w - 20, 180))
            self.ln(5)
            os.remove(temp_path)
        except Exception as e:
            print(f"[X] Failed to load image: {image_url} - {e}")


def extract_content_with_images(soup):
    # Remove unwanted tags
    for tag in soup(["header", "footer", "script", "style", "noscript"]):
        tag.decompose()

    elements = (
        soup.body.find_all(recursive=True)
        if soup.body
        else soup.find_all(recursive=True)
    )

    content_blocks = []

    for tag in elements:
        if tag.name in ["h1", "h2", "h3", "p", "li", "blockquote", "figcaption"]:
            text = tag.get_text(strip=True)
            if text:
                if tag.name == "li":
                    content_blocks.append(("text", f"• {text}"))
                else:
                    content_blocks.append(("text", text))

        elif tag.name == "img":
            src = tag.get("src")
            if src and src.startswith("http"):
                content_blocks.append(("image", src))

    return content_blocks


class ScrapeToPDFView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        url = request.data.get("url", "").strip()
        if not url:
            return Response({"error": "Missing URL."}, status=400)

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Referer": "https://www.google.com/",
            }
            response = requests.get(url, timeout=10, headers=headers)
            if response.status_code != 200:
                return Response({"error": f"Failed to access {url}"}, status=500)

            soup = BeautifulSoup(response.content, "html.parser")
            content = extract_content_with_images(soup)

            if not content:
                return Response({"error": "No usable content found."}, status=404)

            # Generate PDF
            title = soup.title.string if soup.title else "web_content"
            filename = f"{slugify(title)}.pdf"
            filepath = os.path.join("data", filename)
            os.makedirs("data", exist_ok=True)

            pdf = UnicodePDFWithImages()
            for ctype, value in content:
                if ctype == "text":
                    pdf.write_text(value)
                elif ctype == "image":
                    pdf.write_image(value, base_url=url)

            pdf.output(filepath)

            return Response(
                {"message": "PDF with text + images saved.", "file": filepath},
                status=200,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)


import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from keras.models import load_model
import wikipedia


# === Load dữ liệu & mô hình chỉ 1 lần ===
DISEASE_DATA_PATH = "health_10_disease_data.csv"
CNN_PATH = "CNN_model.h5"
RNN_PATH = "RNN_model.h5"
LSTM_PATH = "LSTM_model.h5"

# Load data
disease_data = pd.read_csv(DISEASE_DATA_PATH)
label_encoder = LabelEncoder()
disease_data["Disease"] = label_encoder.fit_transform(disease_data["Disease"])

X = disease_data.drop("Disease", axis=1).values
y = disease_data["Disease"].values

# Normalize
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Load models
cnn_model = load_model(CNN_PATH, compile=False)
rnn_model = load_model(RNN_PATH, compile=False)
lstm_model = load_model(LSTM_PATH, compile=False)

for model in [cnn_model, rnn_model, lstm_model]:
    model.compile(optimizer="adam", loss="mean_squared_error")


# === Dự đoán bệnh ===
def predict_disease(input_data, model_type="RNN"):
    input_scaled = scaler.transform([input_data])
    input_scaled = input_scaled.reshape((1, input_scaled.shape[1], 1))

    if model_type.upper() == "CNN":
        model = cnn_model
    elif model_type.upper() == "RNN":
        model = rnn_model
    else:
        model = lstm_model

    prediction = model.predict(input_scaled)
    predicted_disease = label_encoder.inverse_transform(
        np.round(prediction).astype(int)
    )
    return predicted_disease[0]


# === Lấy mô tả bệnh ===
def get_disease_info(disease_name):
    try:
        return wikipedia.summary(disease_name, sentences=3, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError:
        return "Nhiều kết quả tương tự. Vui lòng xác định rõ tên bệnh hơn."
    except wikipedia.exceptions.PageError:
        return "Không tìm thấy thông tin bệnh trên Wikipedia."
    except Exception as e:
        return f"Lỗi khi lấy thông tin bệnh: {str(e)}"


# === API View ===
class PredictDiseaseChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Nhận dữ liệu từ request
            input_data = [
                float(request.data.get("age")),
                float(request.data.get("blood_pressure")),
                float(request.data.get("cholesterol")),
                float(request.data.get("bmi")),
                float(request.data.get("blood_sugar")),
                float(request.data.get("creatinine")),
            ]
            model_type = request.data.get("model_type", "RNN")

            # Dự đoán bệnh
            predicted = predict_disease(input_data, model_type)
            disease_info = get_disease_info(predicted)

            vietnamese_predicted = translate_to_vietnamese(predicted)
            vietnamese_disease_info = translate_to_vietnamese(disease_info)

            return Response(
                {
                    "predicted_disease": vietnamese_predicted,
                    "disease_info": vietnamese_disease_info,
                },
                status=200,
            )

        except KeyError as e:
            return Response({"error": f"Thiếu trường: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# chatbot_service/views.py (phần thêm API training model)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)
from keras.models import Sequential
from keras.layers import Dense, LSTM, SimpleRNN, Conv1D, MaxPooling1D, Flatten, Dropout
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import os


class TrainModelView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = pd.read_csv("health_10_disease_data.csv")
            label_encoder = LabelEncoder()
            data["Disease"] = label_encoder.fit_transform(data["Disease"])

            X = data.drop("Disease", axis=1).values
            y = data["Disease"].values

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            scaler = MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            X_train_rnn = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
            X_test_rnn = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

            def build_cnn():
                model = Sequential()
                model.add(
                    Conv1D(
                        64,
                        2,
                        activation="relu",
                        input_shape=(X_train.shape[1], 1),
                        padding="same",
                    )
                )
                model.add(MaxPooling1D(2))
                model.add(Conv1D(128, 2, activation="relu", padding="same"))
                model.add(MaxPooling1D(2))
                model.add(Conv1D(256, 2, activation="relu", padding="same"))
                model.add(Flatten())
                model.add(Dense(128, activation="relu"))
                model.add(Dropout(0.5))
                model.add(Dense(1))
                model.compile(optimizer=Adam(), loss="mse")
                return model

            def build_rnn():
                model = Sequential()
                model.add(
                    SimpleRNN(
                        64,
                        input_shape=(X_train_rnn.shape[1], 1),
                        activation="relu",
                        return_sequences=True,
                    )
                )
                model.add(SimpleRNN(128, activation="relu", return_sequences=True))
                model.add(SimpleRNN(256, activation="relu", return_sequences=True))
                model.add(SimpleRNN(128, activation="relu", return_sequences=True))
                model.add(SimpleRNN(64, activation="relu"))
                model.add(Dense(128, activation="relu"))
                model.add(Dense(1))
                model.compile(optimizer=Adam(), loss="mse")
                return model

            def build_lstm():
                model = Sequential()
                model.add(
                    LSTM(
                        64, input_shape=(X_train_rnn.shape[1], 1), return_sequences=True
                    )
                )
                model.add(LSTM(128, return_sequences=True))
                model.add(LSTM(256, return_sequences=True))
                model.add(LSTM(128, return_sequences=True))
                model.add(LSTM(64, return_sequences=False))
                model.add(Dense(128, activation="relu"))
                model.add(Dense(1))
                model.compile(optimizer=Adam(), loss="mse")
                return model

            models = {"CNN": build_cnn(), "RNN": build_rnn(), "LSTM": build_lstm()}
            errors = {}

            for name, model in models.items():
                if name == "CNN":
                    X_train_input = X_train.reshape(
                        (X_train.shape[0], X_train.shape[1], 1)
                    )
                    X_test_input = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
                else:
                    X_train_input = X_train_rnn
                    X_test_input = X_test_rnn

                history = model.fit(
                    X_train_input,
                    y_train,
                    epochs=100,
                    batch_size=64,
                    validation_data=(X_test_input, y_test),
                    verbose=0,
                )

                y_pred = model.predict(X_test_input)
                mae = mean_absolute_error(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                mape = mean_absolute_percentage_error(y_test, y_pred)

                errors[name] = {"MAE": mae, "MSE": mse, "RMSE": rmse, "MAPE": mape}

                model.save(f"{name}_model.h5")

            return Response(
                {
                    "message": "Models trained and saved successfully.",
                    "metrics": errors,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateDataView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            num_samples = int(
                request.data.get("num_samples", 20000)
            )  # cho phép truyền số lượng mẫu

            np.random.seed(42)

            age = np.random.randint(18, 80, size=num_samples)
            blood_pressure = np.random.randint(90, 180, size=num_samples)
            cholesterol = np.random.randint(150, 300, size=num_samples)
            bmi = np.random.uniform(18.5, 40, size=num_samples)
            blood_sugar = np.random.randint(70, 200, size=num_samples)
            creatinine = np.random.uniform(0.5, 2.5, size=num_samples)

            disease_heart = (blood_pressure > 140) | (cholesterol > 250)
            disease_diabetes = blood_sugar > 150
            disease_hypertension = blood_pressure > 160
            disease_obesity = bmi > 30
            disease_kidney = creatinine > 1.5
            disease_cancer = (age > 50) & (cholesterol > 250)
            disease_dyslipidemia = cholesterol > 240
            disease_type2_diabetes = (blood_sugar > 130) & (age > 40)
            disease_metabolic_syndrome = (bmi > 30) & (blood_pressure > 140)
            disease_arthritis = (age > 45) & (bmi > 25)

            disease = np.select(
                [
                    disease_heart,
                    disease_diabetes,
                    disease_hypertension,
                    disease_obesity,
                    disease_kidney,
                    disease_cancer,
                    disease_dyslipidemia,
                    disease_type2_diabetes,
                    disease_metabolic_syndrome,
                    disease_arthritis,
                ],
                [
                    "Heart Disease",
                    "Diabetes",
                    "Hypertension",
                    "Obesity",
                    "Kidney Disease",
                    "Cancer",
                    "Dyslipidemia",
                    "Type 2 Diabetes",
                    "Metabolic Syndrome",
                    "Arthritis",
                ],
                default="No Disease",
            )

            data = pd.DataFrame(
                {
                    "Age": age,
                    "Blood Pressure": blood_pressure,
                    "Cholesterol": cholesterol,
                    "BMI": bmi,
                    "Blood Sugar": blood_sugar,
                    "Creatinine": creatinine,
                    "Disease": disease,
                }
            )

            output_path = "health_10_disease_data.csv"
            data.to_csv(output_path, index=False)

            return Response(
                {
                    "message": "Synthetic health data generated successfully.",
                    "file": output_path,
                    "samples": num_samples,
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
