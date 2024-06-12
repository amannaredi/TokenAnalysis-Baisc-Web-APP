from flask import Flask, request, render_template, jsonify
import openai
from openai import OpenAI
import os
from config import Config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail configuration
app.config.from_object(Config)

mail = Mail(app)

openai.api_key = app.config['OPENAI_API_KEY']

# OpenAI API setup

def analyze_token_project(form_data):
    prompt = f"""
    Analyze this small-cap token project:
    Token Name: {form_data['token_name']}
    Token Symbol: {form_data['token_symbol']}
    Website: {form_data['website_url']}
    Technology: {form_data['technology']}
    Roadmap and Key Milestones: {form_data['roadmap']}
    Whitepaper URL: {form_data['whitepaper_url']}
    Total supply and Circulating supply: {form_data['supply']}
    Token Distribution:
    - Founders: {form_data['founders']}
    - Developers: {form_data['developers']}
    - Marketing: {form_data['marketing']}
    - Community: {form_data['community']}
    - Investors: {form_data['investors']}
    Vesting Schedules: {form_data['vesting']}
    Use Cases: {form_data['use_cases']}
    Incentives: {form_data['incentives']}
    Mechanisms: {form_data['mechanisms']}
    Economic Sustainability: {form_data['sustainability']}
    Audit Report URL: {form_data['audit_url']}
    Audit Summary: {form_data['audit_summary']}
    Total Liquidity and lockup duration: {form_data['liquidity']}
    Current Market Capitalization: {form_data['market_cap']}
    Team Expertise:
    - CEO/ Founder: {form_data['ceo']}
    - CFO: {form_data['cfo']}
    - CTO: {form_data['cto']}
    - CMO: {form_data['cmo']}
    - Developer: {form_data['developer']}
    Team Roles with LinkedIn profiles: {form_data['linkedin_profiles']}
    Academic Background: {form_data['academic_background']}
    Community Engagement on Social Media:
    - Twitter: {form_data['twitter']}
    - Telegram: {form_data['telegram']}
    - Discord: {form_data['discord']}
    - LinkedIn: {form_data['linkedin']}
    - Facebook: {form_data['facebook']}
    - Twitch: {form_data['twitch']}
    - TikTok: {form_data['tiktok']}
    Provide Social media links: {form_data['social_links']}
    Provide Link tree link: {form_data['link_tree']}
    User Reviews: {form_data['user_reviews']}
    YouTube URL (if any): {form_data['youtube_url']}
    Marketing Efforts: {form_data['marketing_efforts']}
    Brand Identity: {form_data['brand_identity']}
    Target Audience Reach: {form_data['target_audience']}
    List of Competitors: {form_data['competitors']}
    Advantages/Disadvantages: {form_data['advantages']}
    Unique Selling Propositions (USPs): {form_data['usps']}
    Short-Term vs Long-Term Focus: {form_data['focus']}
    Revenue Streams: {form_data['revenue_streams']}
    Model Sustainability and feasibility: {form_data['model_sustainability']}
    Funding Sources: {form_data['funding_sources']}
    List of Key Partners and describe any collaborations with established players: {form_data['key_partners']}
    Pitch Deck: {form_data['pitch_deck']}
    Anything Else We Should Know? {form_data['additional_info']}
    """
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=500)
    return response.choices[0].message.content.strip()

def send_email_report(form_data, ai_analysis):
    email_address = form_data["email"]
    mail_server = "smtp.googlemail.com"
    mail_port = 587
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    subject = f"AI Analysis for {form_data['token_name']} ({form_data['token_symbol']})"
    body = f"""
    Here is the AI analysis for your token project submission:
    Token Name: {form_data['token_name']}
    Token Symbol: {form_data['token_symbol']}
    Website: {form_data['website_url']}
    Technology: {form_data['technology']}
    Roadmap and Key Milestones: {form_data['roadmap']}
    Whitepaper URL: {form_data['whitepaper_url']}
    Total supply and Circulating supply: {form_data['supply']}
    Token Distribution:
    - Founders: {form_data['founders']}
    - Developers: {form_data['developers']}
    - Marketing: {form_data['marketing']}
    - Community: {form_data['community']}
    - Investors: {form_data['investors']}
    Vesting Schedules: {form_data['vesting']}
    Use Cases: {form_data['use_cases']}
    Incentives: {form_data['incentives']}
    Mechanisms: {form_data['mechanisms']}
    Economic Sustainability: {form_data['sustainability']}
    Audit Report URL: {form_data['audit_url']}
    Audit Summary: {form_data['audit_summary']}
    Total Liquidity and lockup duration: {form_data['liquidity']}
    Current Market Capitalization: {form_data['market_cap']}
    Team Expertise:
    - CEO/ Founder: {form_data['ceo']}
    - CFO: {form_data['cfo']}
    - CTO: {form_data['cto']}
    - CMO: {form_data['cmo']}
    - Developer: {form_data['developer']}
    Team Roles with LinkedIn profiles: {form_data['linkedin_profiles']}
    Academic Background: {form_data['academic_background']}
    Community Engagement on Social Media:
    - Twitter: {form_data['twitter']}
    - Telegram: {form_data['telegram']}
    - Discord: {form_data['discord']}
    - LinkedIn: {form_data['linkedin']}
    - Facebook: {form_data['facebook']}
    - Twitch: {form_data['twitch']}
    - TikTok: {form_data['tiktok']}
    Provide Social media links: {form_data['social_links']}
    Provide Link tree link: {form_data['link_tree']}
    User Reviews: {form_data['user_reviews']}
    YouTube URL (if any): {form_data['youtube_url']}
    Marketing Efforts: {form_data['marketing_efforts']}
    Brand Identity: {form_data['brand_identity']}
    Target Audience Reach: {form_data['target_audience']}
    List of Competitors: {form_data['competitors']}
    Advantages/Disadvantages: {form_data['advantages']}
    Unique Selling Propositions (USPs): {form_data['usps']}
    Short-Term vs Long-Term Focus: {form_data['focus']}
    Revenue Streams: {form_data['revenue_streams']}
    Model Sustainability and feasibility: {form_data['model_sustainability']}
    Funding Sources: {form_data['funding_sources']}
    List of Key Partners and describe any collaborations with established players: {form_data['key_partners']}
    Pitch Deck: {form_data['pitch_deck']}
    Anything Else We Should Know? {form_data['additional_info']}
    
    AI Analysis:
    {ai_analysis}
    """

    message = MIMEMultipart()
    message['From'] = mail_username
    message['To'] = email_address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Setup SMTP connection
    server = smtplib.SMTP(mail_server, mail_port)
    server.starttls()
    server.login(mail_username, mail_password)

    # Send email
    server.send_message(message)

    # Close SMTP connection
    server.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    ai_analysis = analyze_token_project(form_data)
    send_email_report(form_data, ai_analysis)
    return jsonify({"message": "Analysis complete and email sent.", "ai_analysis": ai_analysis})

if __name__ == '__main__':
    app.run(debug=True)
