![Social News Bot Banner](https://raw.githubusercontent.com/ZainulabdeenOfficial/social-news-bot/main/LogoBot.png)

# 🤖 AI News Agent (Gemini Edition)

Автоматический агент: собирает тех‑новости (RSS), генерирует посты через Gemini API, создаёт изображения (локально, бесплатно) и публикует в соцсети по расписанию. Есть веб‑дашборд (Streamlit) и Docker.

## 🚀 Быстрый старт

Самое простое (без затрат): локально через Docker или напрямую Python.

### Вариант A: Docker
```bash
cp env_template.txt .env  # заполните ключи
docker compose up -d --build
# Откройте дашборд: http://localhost:8501
```

### Вариант B: Python
```bash
pip install -r requirements.txt
cp env_template.txt .env  # заполните ключи
streamlit run web_dashboard.py
# или автопостинг 24/7
python main.py run
```

## ✨ Возможности

- 📰 **Automated News Fetching**: Fetches latest tech news from multiple sources
- 🤖 **AI‑генерация контента**: с помощью Gemini API (google‑generativeai)
- 🎨 **Изображения**: локальная генерация (Pillow, бесплатно), оптимизация под платформы
- 📱 **Multi-Platform Posting**: Posts to LinkedIn, Twitter, Facebook
- ⏰ **Smart Scheduling**: Posts at optimal times for maximum engagement
- 📊 **Dashboard Interface**: Beautiful web interface for monitoring and control
- 🔄 **Continuous Operation**: Runs 24/7 with automated scheduling

## 🛠️ Локальная разработка

### Требования
- Python 3.10+
- Gemini API key
- API‑ключи соцсетей (опционально)

### Установка
```bash
# Clone the repository
git clone https://github.com/ZainulabdeenOfficial/social-news-bot.git
cd social-news-bot

# Установка зависимостей
pip install -r requirements.txt

# Переменные окружения
cp env_template.txt .env
# Заполните .env своими ключами
```

### Использование

#### Веб‑дашборд
```bash
streamlit run web_dashboard.py
```

#### Командная строка
```bash
# Запуск планировщика
python main.py run

# Мгновенная публикация
python main.py post-now

# Получить новости
python main.py fetch-news

# Тест компонентов
python main.py test
```

## 🌐 Deployment Options

### 🟣 Vercel (Recommended)
- ⚡ Lightning fast deployments
- 🌍 Global CDN
- 🔄 Automatic deployments
- 📱 Serverless functions
- 🆓 Generous free tier

### 🚆 Railway
- 🎯 One-click deployment
- 🔧 Easy environment variable management
- 📊 Built-in monitoring
- 🆓 500 hours/month free
- 🔄 GitHub integration

### 🎨 Render
- 🛡️ DDoS protection
- 🔒 Automatic SSL
- 📈 Auto-scaling
- 🆓 750 hours/month free
- 🌐 Custom domains

### 🔵 Heroku
- 🏛️ Established platform
- 🔧 Extensive add-ons
- 📊 Advanced monitoring
- 🆓 550-1000 hours/month free
- 🛠️ CLI tools

**📖 For detailed deployment instructions, see:**
- [Multi-Platform Deployment Guide](MULTI_PLATFORM_DEPLOYMENT.md)
- [Vercel Deployment Guide](VERCEL_DEPLOYMENT_GUIDE.md)
- [Quick Deploy Guide](QUICK_DEPLOY.md)

## 🔧 Конфигурация

### Обязательные переменные окружения
```bash
GEMINI_API_KEY=your-gemini-api-key
```

### Опциональные переменные окружения (соцсети)
```bash
# LinkedIn
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Twitter
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Facebook
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
```

## 📁 Project Structure

```
├── src/
│   ├── config.py             # Настройки и .env
│   ├── main.py               # CLI‑вход
│   ├── scheduler.py          # Планировщик задач
│   ├── ai/
│   │   ├── content_generator.py   # Генерация постов (Gemini)
│   │   └── image_generator.py     # Локальные изображения
│   └── services/
│       ├── news_fetcher.py        # RSS сборщик
│       └── social_media_poster.py # Постинг в соцсети
├── web_dashboard.py          # Streamlit дашборд (импортирует из src)
├── main.py                   # Тонкая обёртка на src.main
├── api/
│   └── index.py             # Serverless эндпоинты (Vercel/иные)
├── tests/                    # pytest‑тесты
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
├── Procfile                 # Heroku configuration
├── railway.json             # Railway configuration
├── render.yaml              # Render configuration
├── runtime.txt              # Python version specification
├── deploy.py               # Universal deployment script
├── deploy_vercel.py        # Vercel-specific deployment script
└── README.md                # This file
```

## 🔍 API (serverless)

### Health Check
```
GET /health
```
Returns service status and version information.

### API Status
```
GET /api/status
```
Returns status of all components (news fetcher, content generator, etc.).

## 🚀 Деплой и бесплатные варианты

- Docker (локально, бесплатно): `docker compose up -d --build` → дашборд на `http://localhost:8501`.
- Railway/Render/Heroku: можно деплоить бесплатно на старте, но фоновые джобы/кроны могут требовать платный план. Рекомендуем локальный Docker или VPS c `docker compose`.
- Планировщик: контейнер `worker` выполняет `python -m src.main run`.

- **Fast Deployment**: Optimized for all major platforms
- **Auto-scaling**: Handles traffic spikes automatically
- **Global CDN**: Content delivered from edge locations
- **99.9% Uptime**: Reliable hosting infrastructure

## 🔒 Безопасность

- **Environment Variables**: Secure API key management
- **HTTPS**: Automatic SSL certificates
- **Input Validation**: All inputs are validated
- **Rate Limiting**: Built-in protection against abuse

## 📊 Мониторинг

- **Health Checks**: Automatic monitoring endpoints
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Real-time performance monitoring
- **Usage Analytics**: Track API usage and performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 Лицензия

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Благодарности

- OpenAI for providing the AI capabilities
- Streamlit for the web framework
- Vercel, Railway, Render, and Heroku for hosting platforms
- All contributors and supporters

## 📞 Поддержка

### Где взять ключи (бесплатно/триалы)
- Gemini API: аккаунт Google → Google AI Studio → создайте API‑ключ, добавьте в `.env` как `GEMINI_API_KEY`.
- LinkedIn/Twitter/Facebook: потребуется регистрация разработчика и создание приложения. Для тестов можно оставить пустыми — публикация будет пропущена, но генерация контента и дашборд будут работать.


- **Documentation**: [MULTI_PLATFORM_DEPLOYMENT.md](MULTI_PLATFORM_DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/ZainulabdeenOfficial/social-news-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ZainulabdeenOfficial/social-news-bot/discussions)

---

**Made with ❤️ by M Zain Ul Abideen**

[![GitHub stars](https://img.shields.io/github/stars/ZainulabdeenOfficial/social-news-bot?style=social)](https://github.com/ZainulabdeenOfficial/social-news-bot)
[![GitHub forks](https://img.shields.io/github/forks/ZainulabdeenOfficial/social-news-bot?style=social)](https://github.com/ZainulabdeenOfficial/social-news-bot)
[![GitHub issues](https://img.shields.io/github/issues/ZainulabdeenOfficial/social-news-bot)](https://github.com/ZainulabdeenOfficial/social-news-bot/issues)
[![GitHub license](https://img.shields.io/github/license/ZainulabdeenOfficial/social-news-bot)](https://github.com/ZainulabdeenOfficial/social-news-bot/blob/main/LICENSE)

