# 繝吶・繧ｹ繧､繝｡繝ｼ繧ｸ・・ython 3.11 縺ｪ縺ｩ縲√Μ繝昴ず繝医Μ縺ｫ蜷医ｏ縺帙※驕ｸ縺ｶ・・
FROM python:3.11-slim

# 菴懈･ｭ繝・ぅ繝ｬ繧ｯ繝医Μ繧偵さ繝ｳ繝・リ蜀・↓菴懈・
WORKDIR /app

# 繝ｪ繝昴ず繝医Μ縺ｮ蜀・ｮｹ繧偵さ繝ｳ繝・リ縺ｮ /app 縺ｫ繧ｳ繝斐・
COPY . .

# Python 縺ｮ萓晏ｭ倥ヱ繝・こ繝ｼ繧ｸ繧偵う繝ｳ繧ｹ繝医・繝ｫ
RUN pip install --no-cache-dir -r requirements.txt

# 繧ｳ繝ｳ繝・リ襍ｷ蜍墓凾縺ｫ螳溯｡後☆繧九さ繝槭Φ繝会ｼ井ｾ具ｼ嗄ain.py 繧貞ｮ溯｡鯉ｼ・
CMD ["python", "src/main.py"]
