from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__, static_folder='.')
CORS(app)

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')
model_name = os.getenv('MODEL_NAME')

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

SYSTEM_PROMPT = """你是一位专业的置信度裁定专家。根据用户提供的环境背景、人物设定和说话内容，进行深入分析并输出置信度裁定报告。

请严格按照以下JSON格式输出结果，不要包含任何其他说明文字：

{
  "credibility_score": 85,
  "credibility_level": "高度可信",
  "analysis_process": "详细分析文本...",
  "reasons": ["理由1", "理由2", "理由3"],
  "suggestions": ["建议1", "建议2"],
  "predictions": [
    {"scenario": "可能情况1描述", "probability": 60},
    {"scenario": "可能情况2描述", "probability": 25},
    {"scenario": "可能情况3描述", "probability": 15}
  ]
}

置信度等级说明：
- 90-100%: 高度可信
- 70-89%: 比较可信
- 50-69%: 存疑
- 30-49%: 高度可疑
- 0-29%: 虚假

请确保predictions中的probability总和为100%。"""


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/credibility_check', methods=['POST'])
def credibility_check():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据为空'}), 400
        
        environment = data.get('environment', '').strip()
        character = data.get('character', '').strip()
        statement = data.get('statement', '').strip()
        
        if not all([environment, character, statement]):
            return jsonify({'error': '请填写所有必填字段'}), 400
        
        user_prompt = f"""环境/背景:
{environment}

人物设定:
{character}

人物说的话:
{statement}

请根据以上信息，进行置信度裁定。"""
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        try:
            result = json.loads(result_text)
            
            required_fields = ['credibility_score', 'credibility_level', 'analysis_process', 'reasons', 'suggestions', 'predictions']
            for field in required_fields:
                if field not in result:
                    raise ValueError(f'缺少必要字段: {field}')
            
            return jsonify(result)
            
        except json.JSONDecodeError:
            return jsonify({'error': 'AI返回格式错误，请重试'}), 500
        except ValueError as e:
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
