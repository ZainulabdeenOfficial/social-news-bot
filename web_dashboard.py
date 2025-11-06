import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List
import time

# Import our modules
from src.config import Config
from src.services.news_fetcher import NewsFetcher
from src.ai.content_generator import ContentGenerator
from src.ai.image_generator import ImageGenerator
from src.services.social_media_poster import SocialMediaPoster
from src.scheduler import NewsAgentScheduler

# Page configuration
st.set_page_config(
    page_title="AI News Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class Dashboard:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_generator = ContentGenerator()
        self.image_generator = ImageGenerator()
        self.social_poster = SocialMediaPoster()
        self.scheduler = NewsAgentScheduler()
    
    def _save_to_env_file(self, key: str, value: str):
        """Save a key-value pair to the .env file"""
        env_file = '.env'
        
        # Read existing .env file
        env_vars = {}
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key_val = line.split('=', 1)
                        if len(key_val) == 2:
                            env_vars[key_val[0]] = key_val[1]
        
        # Update the specific key
        env_vars[key] = value
        
        # Write back to .env file
        with open(env_file, 'w') as f:
            for k, v in env_vars.items():
                f.write(f"{k}={v}\n")
        
        # Reload config to reflect changes
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
    
    def _save_schedule_to_env(self, platform: str, times: List[str]):
        """Save posting schedule to .env file"""
        schedule_key = f"{platform.upper()}_POSTING_SCHEDULE"
        schedule_value = ','.join(times) if times else ''
        self._save_to_env_file(schedule_key, schedule_value)
    
    def _save_system_settings_to_env(self, max_posts: int):
        """Save system settings to .env file"""
        self._save_to_env_file("MAX_POSTS_PER_DAY", str(max_posts))
    
    def run(self):
        """Run the dashboard"""
        # Header
        st.markdown('<h1 class="main-header">🤖 AI News Agent Dashboard</h1>', unsafe_allow_html=True)
        
        # Sidebar
        self.sidebar()
        
        # Main content
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "📰 News Feed", 
            "📝 Content Generator", 
            "📱 Social Media", 
            "⚙️ Settings"
        ])
        
        with tab1:
            self.overview_tab()
        
        with tab2:
            self.news_feed_tab()
        
        with tab3:
            self.content_generator_tab()
        
        with tab4:
            self.social_media_tab()
        
        with tab5:
            self.settings_tab()
    
    def sidebar(self):
        """Sidebar with quick actions and status"""
        st.sidebar.title("🚀 Quick Actions")
        
        # Quick post button
        if st.sidebar.button("📤 Post Now", type="primary"):
            with st.spinner("Posting content..."):
                try:
                    self.scheduler.post_now()
                    st.sidebar.success("Content posted successfully!")
                except Exception as e:
                    st.sidebar.error(f"Error posting: {e}")
        
        # Fetch news button
        if st.sidebar.button("📰 Fetch Latest News"):
            with st.spinner("Fetching news..."):
                try:
                    news = self.news_fetcher.get_recent_news(hours=6)
                    st.sidebar.success(f"Fetched {len(news)} articles!")
                except Exception as e:
                    st.sidebar.error(f"Error fetching news: {e}")
        
        # System status
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔧 System Status")
        
        # Configuration status
        config_status = {
            "OpenAI API": bool(Config.OPENAI_API_KEY),
            "LinkedIn": bool(Config.LINKEDIN_ACCESS_TOKEN),
            "Twitter": bool(Config.TWITTER_API_KEY),
        }
        
        for service, configured in config_status.items():
            status = "✅" if configured else "❌"
            st.sidebar.text(f"{status} {service}")
        
        # Schedule status
        st.sidebar.markdown("---")
        st.sidebar.subheader("⏰ Next Posts")
        
        status = self.scheduler.get_schedule_status()
        for job in status['next_runs'][:3]:  # Show next 3 scheduled jobs
            st.sidebar.text(f"🕐 {job.next_run.strftime('%H:%M')}")
    
    def overview_tab(self):
        """Overview tab with metrics and charts"""
        st.header("📊 System Overview")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📰 Articles Today",
                value=self._get_articles_count(),
                delta=self._get_articles_delta()
            )
        
        with col2:
            st.metric(
                label="📤 Posts Today",
                value=self._get_posts_count(),
                delta=self._get_posts_delta()
            )
        
        with col3:
            st.metric(
                label="🎯 Engagement Rate",
                value=f"{self._get_engagement_rate():.1f}%",
                delta=self._get_engagement_delta()
            )
        
        with col4:
            st.metric(
                label="⏰ Scheduled Jobs",
                value=len(self.scheduler.get_schedule_status()['next_runs'])
            )
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Posting Activity")
            activity_data = self._get_posting_activity_data()
            if activity_data:
                fig = px.line(
                    activity_data, 
                    x='time', 
                    y='posts',
                    title="Posts per Hour (Last 24 Hours)"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No posting activity data available")
        
        with col2:
            st.subheader("🔥 Trending Topics")
            trending_data = self._get_trending_topics_data()
            if trending_data:
                fig = px.bar(
                    trending_data,
                    x='topic',
                    y='count',
                    title="Top Trending Topics"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No trending topics data available")
        
        # Recent activity
        st.subheader("🕒 Recent Activity")
        activity_log = self._get_recent_activity()
        
        if activity_log:
            for activity in activity_log:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        st.text(activity['time'])
                    with col2:
                        st.text(activity['message'])
                    with col3:
                        status_color = {
                            'success': 'status-success',
                            'warning': 'status-warning',
                            'error': 'status-error'
                        }.get(activity['status'], '')
                        st.markdown(f'<span class="{status_color}">{activity["status"].upper()}</span>', unsafe_allow_html=True)
        else:
            st.info("No recent activity")
    
    def news_feed_tab(self):
        """News feed tab showing latest articles"""
        st.header("📰 Latest Tech News")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            hours = st.selectbox(
                "Time Range",
                [6, 12, 24, 48],
                index=2,
                format_func=lambda x: f"{x} hours"
            )
        
        with col2:
            source_filter = st.selectbox(
                "Source",
                ["All"] + [source['name'] for source in Config.NEWS_SOURCES]
            )
        
        with col3:
            if st.button("🔄 Refresh News"):
                st.rerun()
        
        # Fetch and display news
        with st.spinner("Fetching latest news..."):
            try:
                news = self.news_fetcher.get_recent_news(hours=hours)
                
                if source_filter != "All":
                    news = [article for article in news if article['source'] == source_filter]
                
                if not news:
                    st.warning("No news found for the selected criteria")
                    return
                
                st.success(f"Found {len(news)} articles")
                
                # Display articles
                for i, article in enumerate(news):
                    with st.expander(f"{i+1}. {article['title']}", expanded=i<3):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Source:** {article['source']}")
                            st.write(f"**Published:** {article['published']}")
                            st.write(f"**Description:** {article['description']}")
                            st.write(f"**Link:** {article['link']}")
                        
                        with col2:
                            if st.button(f"📤 Post Article {i+1}", key=f"post_{i}"):
                                self._post_article(article)
                        
                        # Show image if available
                        if article.get('image_url'):
                            st.image(article['image_url'], caption="Article Image", use_column_width=True)
                
                # Show trending topics
                st.subheader("🔥 Trending Topics")
                trending = self.news_fetcher.get_trending_topics(news)
                st.write(", ".join([f"#{topic}" for topic in trending[:10]]))
                
            except Exception as e:
                st.error(f"Error fetching news: {e}")
    
    def content_generator_tab(self):
        """Content generator tab for testing and manual generation"""
        st.header("📝 Content Generator")
        
        # Test content generation
        st.subheader("🧪 Test Content Generation")
        
        # Sample article input
        st.write("**Sample Article:**")
        sample_article = {
            'title': st.text_input(
                "Title",
                value="OpenAI Releases GPT-5 with Revolutionary Capabilities"
            ),
            'description': st.text_area(
                "Description",
                value="OpenAI has announced the release of GPT-5, featuring unprecedented reasoning abilities and multimodal understanding.",
                height=100
            ),
            'source': st.selectbox(
                "Source",
                [source['name'] for source in Config.NEWS_SOURCES]
            ),
            'link': st.text_input(
                "Link",
                value="https://example.com/article"
            )
        }
        
        # Platform selection
        platform = st.selectbox(
            "Target Platform",
            ['linkedin', 'twitter', 'facebook']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Generate Content", type="primary"):
                with st.spinner("Generating content..."):
                    try:
                        post_data = self.content_generator.generate_post_content(sample_article, platform)
                        
                        st.success("Content generated successfully!")
                        
                        # Display generated content
                        st.subheader("📝 Generated Content")
                        st.text_area(
                            "Post Text",
                            value=post_data.get('post_text', ''),
                            height=200,
                            disabled=True
                        )
                        
                        st.write("**Hashtags:**", ", ".join(post_data.get('hashtags', [])))
                        st.write("**Call to Action:**", post_data.get('call_to_action', ''))
                        
                    except Exception as e:
                        st.error(f"Error generating content: {e}")
        
        with col2:
            if st.button("🎨 Generate Image"):
                with st.spinner("Generating image..."):
                    try:
                        image_prompt = f"Tech news: {sample_article['title']}"
                        image_path = f"images/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        
                        generated_image = self.image_generator.generate_image(image_prompt, image_path)
                        
                        if generated_image:
                            st.success("Image generated successfully!")
                            st.image(generated_image, caption="Generated Image", use_column_width=True)
                        else:
                            st.error("Failed to generate image")
                            
                    except Exception as e:
                        st.error(f"Error generating image: {e}")
        
        # Content templates
        st.subheader("📋 Content Templates")
        
        template = st.selectbox(
            "Select Template",
            ["Daily Summary", "Breaking News", "Tech Analysis", "Industry Update"]
        )
        
        if st.button("📝 Generate Template Content"):
            with st.spinner("Generating template content..."):
                try:
                    # Generate template-specific content
                    template_content = self._generate_template_content(template, sample_article)
                    st.text_area(
                        "Template Content",
                        value=template_content,
                        height=200,
                        disabled=True
                    )
                except Exception as e:
                    st.error(f"Error generating template: {e}")
    
    def social_media_tab(self):
        """Social media tab for posting and monitoring"""
        st.header("📱 Social Media Management")
        
        # Platform status
        st.subheader("🔧 Platform Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("LinkedIn", "✅ Connected" if Config.LINKEDIN_ACCESS_TOKEN else "❌ Not Connected")
        
        with col2:
            st.metric("Twitter", "✅ Connected" if Config.TWITTER_API_KEY else "❌ Not Connected")
        
        with col3:
            st.metric("Facebook", "✅ Connected" if hasattr(Config, 'FACEBOOK_ACCESS_TOKEN') and Config.FACEBOOK_ACCESS_TOKEN else "❌ Not Connected")
        
        # Manual posting
        st.subheader("📤 Manual Post")
        
        post_text = st.text_area("Post Content", height=150)
        platforms = st.multiselect(
            "Target Platforms",
            ['linkedin', 'twitter', 'facebook'],
            default=['linkedin']
        )
        
        uploaded_file = st.file_uploader("Upload Image (Optional)", type=['png', 'jpg', 'jpeg'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Post Now", type="primary"):
                if post_text:
                    with st.spinner("Posting..."):
                        try:
                            post_data = {
                                'post_text': post_text,
                                'hashtags': [],
                                'call_to_action': ''
                            }
                            
                            results = {}
                            for platform in platforms:
                                success = self.social_poster.post_to_platform(platform, post_data)
                                results[platform] = success
                            
                            # Show results
                            for platform, success in results.items():
                                if success:
                                    st.success(f"✅ Posted to {platform}")
                                else:
                                    st.error(f"❌ Failed to post to {platform}")
                        except Exception as e:
                            st.error(f"Error posting: {e}")
                else:
                    st.warning("Please enter post content")
        
        with col2:
            if st.button("📅 Schedule Post"):
                st.info("Scheduling feature coming soon!")
        
        # Posting schedule
        st.subheader("⏰ Posting Schedule")
        
        schedule_data = []
        for platform, times in Config.POSTING_SCHEDULE.items():
            for time_str in times:
                schedule_data.append({
                    'Platform': platform.title(),
                    'Time': time_str,
                    'Status': 'Scheduled'
                })
        
        if schedule_data:
            df = pd.DataFrame(schedule_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No scheduled posts")
        
        # Recent posts
        st.subheader("📊 Recent Posts")
        
        recent_posts = self._get_recent_posts()
        if recent_posts:
            for post in recent_posts:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{post['platform'].title()}** - {post['time']}")
                        st.write(post['content'][:100] + "...")
                    with col2:
                        st.write(f"Likes: {post.get('likes', 0)}")
                    with col3:
                        st.write(f"Comments: {post.get('comments', 0)}")
        else:
            st.info("No recent posts")
    
    def settings_tab(self):
        """Settings tab for configuration"""
        st.header("⚙️ Settings")
        
        # Configuration Status
        st.subheader("📊 Configuration Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            openai_status = "✅ Configured" if Config.OPENAI_API_KEY else "❌ Not Configured"
            st.metric("OpenAI API", openai_status)
        
        with col2:
            linkedin_status = "✅ Configured" if Config.LINKEDIN_ACCESS_TOKEN else "❌ Not Configured"
            st.metric("LinkedIn", linkedin_status)
        
        with col3:
            twitter_status = "✅ Configured" if Config.TWITTER_ACCESS_TOKEN else "❌ Not Configured"
            st.metric("Twitter", twitter_status)
        
        with col4:
            sources_count = len(Config.NEWS_SOURCES)
            st.metric("News Sources", sources_count)
        
        st.divider()
        
        # API Configuration
        st.subheader("🔑 API Configuration")
        
        with st.expander("OpenAI Configuration", expanded=True):
            openai_key = st.text_input(
                "OpenAI API Key",
                value=Config.OPENAI_API_KEY or "",
                type="password"
            )
            if st.button("Save OpenAI Key"):
                self._save_to_env_file("OPENAI_API_KEY", openai_key)
                st.success("OpenAI key saved!")
        
        with st.expander("LinkedIn Configuration"):
            linkedin_client_id = st.text_input("LinkedIn Client ID", value=Config.LINKEDIN_CLIENT_ID or "")
            linkedin_client_secret = st.text_input("LinkedIn Client Secret", value=Config.LINKEDIN_CLIENT_SECRET or "", type="password")
            linkedin_access_token = st.text_input("LinkedIn Access Token", value=Config.LINKEDIN_ACCESS_TOKEN or "", type="password")
            
            if st.button("Save LinkedIn Settings"):
                self._save_to_env_file("LINKEDIN_CLIENT_ID", linkedin_client_id)
                self._save_to_env_file("LINKEDIN_CLIENT_SECRET", linkedin_client_secret)
                self._save_to_env_file("LINKEDIN_ACCESS_TOKEN", linkedin_access_token)
                st.success("LinkedIn settings saved!")
        
        with st.expander("Twitter Configuration"):
            twitter_api_key = st.text_input("Twitter API Key", value=Config.TWITTER_API_KEY or "")
            twitter_api_secret = st.text_input("Twitter API Secret", value=Config.TWITTER_API_SECRET or "", type="password")
            twitter_access_token = st.text_input("Twitter Access Token", value=Config.TWITTER_ACCESS_TOKEN or "")
            twitter_access_token_secret = st.text_input("Twitter Access Token Secret", value=Config.TWITTER_ACCESS_TOKEN_SECRET or "", type="password")
            
            if st.button("Save Twitter Settings"):
                self._save_to_env_file("TWITTER_API_KEY", twitter_api_key)
                self._save_to_env_file("TWITTER_API_SECRET", twitter_api_secret)
                self._save_to_env_file("TWITTER_ACCESS_TOKEN", twitter_access_token)
                self._save_to_env_file("TWITTER_ACCESS_TOKEN_SECRET", twitter_access_token_secret)
                st.success("Twitter settings saved!")
        
        # Posting Schedule
        st.subheader("⏰ Posting Schedule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**LinkedIn Schedule:**")
            linkedin_times = st.multiselect(
                "LinkedIn posting times",
                ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"],
                default=Config.POSTING_SCHEDULE.get('linkedin', [])
            )
        
        with col2:
            st.write("**Twitter Schedule:**")
            twitter_times = st.multiselect(
                "Twitter posting times",
                ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"],
                default=Config.POSTING_SCHEDULE.get('twitter', [])
            )
        
        if st.button("Save Schedule"):
            self._save_schedule_to_env("linkedin", linkedin_times)
            self._save_schedule_to_env("twitter", twitter_times)
            st.success("Schedule saved!")
        
        # News Sources
        st.subheader("📰 News Sources")
        
        # Display current sources
        sources_df = pd.DataFrame(Config.NEWS_SOURCES)
        st.write("**Current News Sources:**")
        st.dataframe(sources_df, use_container_width=True)
        
        # Add new source
        st.write("**Add New News Source:**")
        col1, col2 = st.columns(2)
        
        with col1:
            new_source_name = st.text_input("Source Name (e.g., TechCrunch)")
            new_source_url = st.text_input("RSS URL")
        
        with col2:
            new_source_category = st.selectbox("Category", ["Technology", "AI", "Startups", "Cybersecurity", "Cloud Computing"])
            new_source_priority = st.slider("Priority (1-10)", 1, 10, 5)
        
        if st.button("Add News Source") and new_source_name and new_source_url:
            # This would need to be implemented to save to config
            st.success(f"Added {new_source_name} as a news source!")
            st.info("Note: News sources are currently read-only. To add permanent sources, edit the config.py file.")
        
        # System settings
        st.subheader("🔧 System Settings")
        
        max_posts = st.slider("Max Posts per Day", 1, 20, Config.MAX_POSTS_PER_DAY)
        
        if st.button("Save System Settings"):
            self._save_system_settings_to_env(max_posts)
            st.success("System settings saved!")
        
        # Test Connections
        st.subheader("🔍 Test Connections")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Test OpenAI"):
                try:
                    # Test OpenAI connection
                    test_response = self.content_generator.generate_post_content(
                        "Test article about AI technology",
                        "This is a test article to verify OpenAI API connection.",
                        "linkedin"
                    )
                    if test_response:
                        st.success("✅ OpenAI connection successful!")
                    else:
                        st.error("❌ OpenAI connection failed!")
                except Exception as e:
                    st.error(f"❌ OpenAI connection failed: {str(e)}")
        
        with col2:
            if st.button("Test LinkedIn"):
                try:
                    # Test LinkedIn connection
                    if Config.LINKEDIN_ACCESS_TOKEN:
                        st.success("✅ LinkedIn credentials configured!")
                    else:
                        st.error("❌ LinkedIn credentials not configured!")
                except Exception as e:
                    st.error(f"❌ LinkedIn connection failed: {str(e)}")
        
        with col3:
            if st.button("Test Twitter"):
                try:
                    # Test Twitter connection
                    if Config.TWITTER_ACCESS_TOKEN:
                        st.success("✅ Twitter credentials configured!")
                    else:
                        st.error("❌ Twitter credentials not configured!")
                except Exception as e:
                    st.error(f"❌ Twitter connection failed: {str(e)}")
    
    # Helper methods
    def _get_articles_count(self):
        """Get articles count for today"""
        try:
            news = self.news_fetcher.get_recent_news(hours=24)
            return len(news)
        except:
            return 0
    
    def _get_articles_delta(self):
        """Get articles delta from yesterday"""
        try:
            yesterday_news = self.news_fetcher.get_recent_news(hours=48)
            today_news = self.news_fetcher.get_recent_news(hours=24)
            return len(today_news) - (len(yesterday_news) - len(today_news))
        except:
            return 0
    
    def _get_posts_count(self):
        """Get posts count for today"""
        # This would come from a database in a real implementation
        return 5
    
    def _get_posts_delta(self):
        """Get posts delta from yesterday"""
        return 2
    
    def _get_engagement_rate(self):
        """Get engagement rate"""
        return 15.5
    
    def _get_engagement_delta(self):
        """Get engagement rate delta"""
        return 2.3
    
    def _get_posting_activity_data(self):
        """Get posting activity data for chart"""
        # Mock data - in real implementation this would come from database
        return pd.DataFrame({
            'time': pd.date_range(start=datetime.now() - timedelta(hours=24), periods=24, freq='H'),
            'posts': [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        })
    
    def _get_trending_topics_data(self):
        """Get trending topics data for chart"""
        # Mock data - in real implementation this would come from analysis
        return pd.DataFrame({
            'topic': ['AI', 'Machine Learning', 'Blockchain', 'Cloud Computing', 'Cybersecurity'],
            'count': [15, 12, 8, 6, 4]
        })
    
    def _get_recent_activity(self):
        """Get recent activity log"""
        # Mock data - in real implementation this would come from logs
        return [
            {'time': '10:30', 'message': 'Posted to LinkedIn', 'status': 'success'},
            {'time': '09:15', 'message': 'Generated content for 5 articles', 'status': 'success'},
            {'time': '08:45', 'message': 'Fetched 12 new articles', 'status': 'success'},
            {'time': '08:00', 'message': 'Daily news fetch completed', 'status': 'success'},
        ]
    
    def _post_article(self, article):
        """Post a specific article"""
        with st.spinner("Posting article..."):
            try:
                self.scheduler.post_now()
                st.success("Article posted successfully!")
            except Exception as e:
                st.error(f"Error posting article: {e}")
    
    def _generate_template_content(self, template, article):
        """Generate template-specific content"""
        templates = {
            "Daily Summary": f"📰 Today's Tech Roundup:\n\n{article['title']}\n\n{article['description']}\n\n#TechNews #DailySummary",
            "Breaking News": f"🚨 BREAKING: {article['title']}\n\n{article['description']}\n\n#BreakingNews #Tech",
            "Tech Analysis": f"🔍 Tech Analysis: {article['title']}\n\n{article['description']}\n\nWhat are your thoughts? #TechAnalysis",
            "Industry Update": f"📈 Industry Update: {article['title']}\n\n{article['description']}\n\n#IndustryUpdate #Technology"
        }
        return templates.get(template, "Template not found")
    
    def _get_recent_posts(self):
        """Get recent posts data"""
        # Mock data - in real implementation this would come from social media APIs
        return [
            {'platform': 'linkedin', 'time': '2 hours ago', 'content': 'Exciting news in AI technology...', 'likes': 45, 'comments': 12},
            {'platform': 'twitter', 'time': '4 hours ago', 'content': 'Breaking: New tech developments...', 'likes': 23, 'comments': 8},
        ]

def main():
    dashboard = Dashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
