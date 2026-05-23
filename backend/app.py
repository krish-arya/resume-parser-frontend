import pdfplumber
import os
from dotenv import load_dotenv
from groq import Groq
from typing import List
import json
from pydantic import BaseModel
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid
import traceback
import zipfile
import tempfile
from datetime import datetime
from bs4 import BeautifulSoup

load_dotenv()

# Initialize APIs - ONLY GROQ
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("ERROR: GROQ_API_KEY not found!")
    exit(1)

groq_client = Groq(api_key=groq_api_key)
print("GROQ client initialized successfully")

class Project(BaseModel):
    project_name: str
    about_project: str
    skills_used: list[str]

class Achivements(BaseModel):
    Achivement_name: str
    institute_name: str
    about: str

class Experience(BaseModel):
    Position_name: str
    Company_name: str
    start_date: str
    end_date: str
    skills_used: list[str]

class Education(BaseModel):
    Institute_name: str
    Degree_name: str
    start_time: str
    end_time: str
    marks: str

class Position_of_Responsibility(BaseModel):
    Position_name: str
    Society_name: str
    Description: str

class Candidate(BaseModel):
    name: str
    job_title: str
    hero_description: str  # NEW
    about_description: str  # NEW
    Education: List[Education]
    Projects: List[Project]
    Experience: List[Experience]
    Achivements: List[Achivements]
    Skills: List[str]
    Position_of_Responsibility: List[Position_of_Responsibility]
    Contact_Info: dict

def get_all_info(info: str) -> Candidate:
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a resume parser and website content generator. "
                        "Extract all structured information from the resume, and also generate:\n"
                        "- hero_description: A 1-2 sentence summary for the hero section, highlighting the candidate's strengths and unique value.\n"
                        "- about_description: A 3-4 sentence engaging about section, summarizing the candidate's background, skills, and what makes them stand out.\n"
                        "IMPORTANT: All text should be in the candidate's voice and based on the resume content.\n"
                        f"The JSON object must use the schema: {json.dumps(Candidate.schema(), indent=2)}"
                    ),
                },
                {
                    "role": "user",
                    "content": f"Extract all information and generate the descriptions from this resume: {info}",
                },
            ],
            model="llama-3.3-70b-versatile",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )
        return Candidate.parse_raw(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Error in resume parsing: {str(e)}")
        raise e

'''def modify_component_with_groq(component_html: str, instructions: str, component_type: str) -> str:
    """Use GROQ to modify HTML component based on instructions"""
    try:
        print(f"Using GROQ to modify component: {component_type}")
        
        prompt = f"""You are an expert web developer. Modify the following HTML component based on the user's instructions.

CRITICAL RULES:
1. Keep ALL existing CSS classes and data attributes EXACTLY as they are
2. Keep the overall HTML structure intact  
3. Only modify content, add inline styles, or change existing inline styles
4. Return ONLY the modified HTML, no explanations, no markdown formatting
5. Ensure the HTML is valid and properly formatted
6. Do not remove or change any data-component attributes
7. Do not change the root element tag name
8. Preserve all existing attributes like id, class, data-*, etc.

Current HTML component:
{component_html}

Component type: {component_type}
User instructions: {instructions}

Return the modified HTML (no markdown, no explanations):"""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert web developer. Return only the modified HTML code without any markdown formatting or explanations."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            stream=False
        )
        
        modified_html = chat_completion.choices[0].message.content.strip()
        
        # Clean up any markdown formatting
        if '\`\`\`html' in modified_html:
            modified_html = modified_html.split('\`\`\`html')[1].split('\`\`\`')[0].strip()
        elif '\`\`\`' in modified_html:
            parts = modified_html.split('\`\`\`')
            if len(parts) >= 3:
                modified_html = parts[1].strip()
        
        # Ensure data-component attribute is preserved
        if 'data-component=' not in modified_html and component_type:
            print("Adding back missing data-component attribute")
            if modified_html.startswith('<'):
                tag_end = modified_html.find('>')
                if tag_end > 0:
                    tag_part = modified_html[:tag_end]
                    rest_part = modified_html[tag_end:]
                    modified_html = f'{tag_part} data-component="{component_type}"{rest_part}'
        
        print(f" GROQ modification completed successfully")
        return modified_html
        
    except Exception as e:
        print(f"GROQ modification error: {str(e)}")
        raise e
'''
def generate_website_code(data, style="professional"):
    """Generate complete website code based on parsed resume data and selected style"""
    
    templates = {
        "professional": {
            "colors": {
                "primary": "#3b82f6",
                "secondary": "#1e40af", 
                "accent": "#f59e0b",
                "background": "#ffffff",
                "text": "#1f2937",
                "light": "#f8fafc",
                "dark": "#0f172a"
            },
            "fonts": "font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;",
            "style_class": "professional"
        },
        "futuristic": {
            "colors": {
                "primary": "#00ffff",
                "secondary": "#ff00ff",
                "accent": "#ffff00", 
                "background": "#0a0a0a",
                "text": "#ffffff",
                "light": "#1a1a2e",
                "dark": "#16213e"
            },
            "fonts": "font-family: 'Orbitron', 'Courier New', monospace;",
            "style_class": "futuristic"
        },
        "playful": {
            "colors": {
                "primary": "#ff6b6b",
                "secondary": "#4ecdc4",
                "accent": "#ffe66d",
                "background": "#fff5f5", 
                "text": "#2d3748",
                "light": "#fef5e7",
                "dark": "#744c9e"
            },
            "fonts": "font-family: 'Poppins', 'Comic Sans MS', cursive;",
            "style_class": "playful"
        }
    }
    
    theme = templates.get(style, templates["professional"])
    
    # Generate HTML with stunning design
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', 'Portfolio')} - {data.get('job_title', 'Professional')}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        {generate_css_content(theme, style)}
    </style>
</head>
<body class="{theme['style_class']}">
    {generate_background_elements(style)}
    
    <div class="container">
        <!-- Navigation -->
        <nav class="navbar" id="navbar">
            <div class="nav-brand">
                <div class="brand-icon">{data.get('name', 'User')[:1].upper()}</div>
                <span class="brand-text">{data.get('name', 'Portfolio')}</span>
            </div>
            <div class="nav-links">
                <a href="#hero" class="nav-link active">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#experience" class="nav-link">Experience</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#skills" class="nav-link">Skills</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
            <div class="nav-toggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero" id="hero">
            <div class="hero-content">
                <div class="hero-text">
                    <h1 class="hero-title" data-component="hero-title">
                        <span class="title-line">Hello, I'm</span>
                        <span class="title-name">{data.get('name', 'Your Name')}</span>
                        <span class="title-role">{data.get('job_title', 'Professional')}</span>
                    </h1>
                    <p class="hero-description" data-component="hero-description">
                        {data.get('hero_description', '')}
                    </p>
                    <div class="hero-buttons" data-component="hero-buttons">
                        <a href="#projects" class="btn btn-primary">View My Work</a>
                        <a href="#contact" class="btn btn-secondary">Get In Touch</a>
                    </div>
                </div>
                <div class="hero-image"> 
                    <div class="profile-card" data-component="profile-card">
                        <div class="profile-avatar">
                            <div class="avatar-inner">{data.get('name', 'User')[:2].upper()}</div>
                            <div class="avatar-ring"></div>
                        </div>
                        <div class="profile-info">
                            <h3>{data.get('name', 'Your Name')}</h3>
                            <p>{data.get('job_title', 'Professional')}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="scroll-indicator">
                <div class="scroll-arrow"></div>
            </div>
        </section>

        <!-- About Section -->
        <section class="section about-section" id="about">
            <div class="section-header" data-component="about-header">
                <h2 class="section-title">About Me</h2>
                <p class="section-subtitle">Discover my journey and passion</p>
            </div>
            <div class="about-content">
                <div class="about-text" data-component="about-text">
                    <h3>{data.get('job_title', 'Professional')} & Problem Solver</h3>
                    <p>{data.get('about_description', '')}</p>
                    <div class="about-stats">
                        <div class="stat-item">
                            <div class="stat-number">{len(data.get('projects', []))}</div>
                            <div class="stat-label">Projects</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{len(data.get('Experience', []))}</div>
                            <div class="stat-label">Experience</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{len(data.get('skills', []))}</div>
                            <div class="stat-label">Skills</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Experience Section -->
        <section class="section experience-section" id="experience">
            <div class="section-header" data-component="experience-header">
                <h2 class="section-title">Experience</h2>
                <p class="section-subtitle">My professional journey</p>
            </div>
            <div class="timeline">
                {generate_experience_html(data.get('Experience', []))}
            </div>
        </section>

        <!-- Projects Section -->
        <section class="section projects-section" id="projects">
            <div class="section-header" data-component="projects-header">
                <h2 class="section-title">Featured Projects</h2>
                <p class="section-subtitle">Some of my recent work</p>
            </div>
            <div class="projects-grid">
                {generate_projects_html(data.get('projects', []))}
            </div>
        </section>

        <!-- Skills Section -->
        <section class="section skills-section" id="skills">
            <div class="section-header" data-component="skills-header">
                <h2 class="section-title">Skills & Technologies</h2>
                <p class="section-subtitle">Tools I work with</p>
            </div>
            <div class="skills-container">
                {generate_skills_html(data.get('skills', []))}
            </div>
        </section>

        <!-- Education Section -->
        <section class="section education-section" id="education">
            <div class="section-header" data-component="education-header">
                <h2 class="section-title">Education</h2>
                <p class="section-subtitle">Academic background</p>
            </div>
            <div class="education-grid">
                {generate_education_html(data.get('education', []))}
            </div>
        </section>

        <!-- Contact Section -->
        <section class="section contact-section" id="contact">
            <div class="section-header" data-component="contact-header">
                <h2 class="section-title">Get In Touch</h2>
                <p class="section-subtitle">Let's work together</p>
            </div>
            <div class="contact-content">
                <div class="contact-info">
                    {generate_contact_html(data.get('Contact_Info', {}))}
                </div>
                <div class="contact-form" data-component="contact-form">
                    <form class="form">
                        <div class="form-group">
                            <input type="text" placeholder="Your Name" class="form-input">
                        </div>
                        <div class="form-group">
                            <input type="email" placeholder="Your Email" class="form-input">
                        </div>
                        <div class="form-group">
                            <textarea placeholder="Your Message" class="form-textarea"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                </div>
            </div>
        </section>
    </div>

    <script>
        {generate_js_content(style)}
    </script>
</body>
</html>"""

    # Assign UUIDs to all [data-component] elements
    soup = BeautifulSoup(html_content, "html.parser")
    for el in soup.find_all(attrs={"data-component": True}):
        el["data-edit-id"] = str(uuid.uuid4())
    html_content = str(soup)
    
    # Generate separate CSS and JS files (for download)
    css_content = generate_css_content(theme, style)
    js_content = generate_js_content(style)
    
    return {
        "html": html_content,
        "css": css_content,
        "js": js_content
    }

def generate_background_elements(style):
    if style == "futuristic":
        return """
        <div class="bg-animation">
            <div class="stars"></div>
            <div class="particles"></div>
            <div class="grid-overlay"></div>
        </div>
        """
    elif style == "playful":
        return """
        <div class="bg-animation">
            <div class="floating-shapes">
                <div class="shape shape-1"></div>
                <div class="shape shape-2"></div>
                <div class="shape shape-3"></div>
                <div class="shape shape-4"></div>
                <div class="shape shape-5"></div>
            </div>
        </div>
        """
    else:
        return """
        <div class="bg-animation">
            <div class="gradient-orbs">
                <div class="orb orb-1"></div>
                <div class="orb orb-2"></div>
                <div class="orb orb-3"></div>
            </div>
        </div>
        """

def generate_experience_html(experiences):
    if not experiences:
        return '<div class="timeline-item" data-component="experience-item"><div class="timeline-content"><h3>No experience data available</h3></div></div>'
    
    html = ""
    for i, exp in enumerate(experiences):
        html += f"""
        <div class="timeline-item" data-component="experience-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <div class="timeline-date">{exp.get('start_date')} - {exp.get('end_date')}</div>
                <h3 class="timeline-title">{exp.get('Position', 'Unknown Position')}</h3>
                <h4 class="timeline-company">{exp.get('Company', 'Unknown Company')}</h4>
                <p class="timeline-description">Led development of innovative solutions and collaborated with cross-functional teams to deliver exceptional results.</p>
                <div class="timeline-skills">
                    {' '.join([f'<span class="skill-chip">{skill}</span>' for skill in exp.get('Skills', [])])}
                </div>
            </div>
        </div>
        """
    return html

def generate_projects_html(projects):
    if not projects:
        return '<div class="project-card" data-component="project-card"><h3>No projects available</h3></div>'
    
    html = ""
    for i, project in enumerate(projects):
        html += f"""
        <div class="project-card" data-component="project-card">
            <div class="project-image">
                <div class="project-overlay">
                    <div class="project-links">
                        <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                        <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                    </div>
                </div>
            </div>
            <div class="project-content">
                <h3 class="project-title">{project.get('title', 'Untitled Project')}</h3>
                <p class="project-description">{project.get('desc', 'No description available')}</p>
                <div class="project-tech">
                    {' '.join([f'<span class="tech-tag">{tech}</span>' for tech in project.get('tech', [])])}
                </div>
            </div>
        </div>
        """
    return html

def generate_skills_html(skills):
    if not skills:
        return '<div class="skill-category" data-component="skill-category"><h3>No skills available</h3></div>'
    
    # Group skills into categories (simplified)
    categories = {
        "Frontend": [],
        "Backend": [],
        "Tools": [],
        "Other": []
    }
    
    frontend_keywords = ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'typescript']
    backend_keywords = ['python', 'java', 'node', 'php', 'ruby', 'go', 'rust']
    tools_keywords = ['git', 'docker', 'kubernetes', 'aws', 'azure', 'jenkins']
    
    for skill in skills:
        skill_lower = skill.lower()
        if any(keyword in skill_lower for keyword in frontend_keywords):
            categories["Frontend"].append(skill)
        elif any(keyword in skill_lower for keyword in backend_keywords):
            categories["Backend"].append(skill)
        elif any(keyword in skill_lower for keyword in tools_keywords):
            categories["Tools"].append(skill)
        else:
            categories["Other"].append(skill)
    
    html = ""
    for category, category_skills in categories.items():
        if category_skills:
            html += f"""
            <div class="skill-category" data-component="skill-category">
                <h3 class="skill-category-title">{category}</h3>
                <div class="skill-items">
                    {' '.join([f'<div class="skill-item" data-component="skill-item"><span class="skill-name">{skill}</span><div class="skill-bar"><div class="skill-progress"></div></div></div>' for skill in category_skills])}
                </div>
            </div>
            """
    
    return html or '<div class="skill-category" data-component="skill-category"><h3>No skills available</h3></div>'

def generate_education_html(education):
    if not education:
        return '<div class="education-card" data-component="education-card"><h3>No education data available</h3></div>'
    
    html = ""
    for edu in education:
        html += f"""
        <div class="education-card" data-component="education-card">
            <div class="education-icon">
                <i class="fas fa-graduation-cap"></i>
            </div>
            <div class="education-content">
                <h3 class="education-degree">{edu.get('Degree_name', 'Unknown Degree')}</h3>
                <h4 class="education-school">{edu.get('Institute_name', 'Unknown Institute')}</h4>
                <p class="education-grade">Grade: {edu.get('Marks', 'N/A')}</p>
                <div class="education-year">{edu.get('start_date')} - {edu.get('end_date')}</div>
            </div>
        </div>
        """
    return html

def generate_contact_html(contact_info):
    if not contact_info:
        return '<div class="contact-item" data-component="contact-item"><p>No contact information available</p></div>'
    
    html = ""
    icons = {
        'email': 'fas fa-envelope',
        'phone': 'fas fa-phone',
        'linkedin': 'fab fa-linkedin',
        'github': 'fab fa-github',
        'location': 'fas fa-map-marker-alt'
    }
    
    for key, value in contact_info.items():
        key_lower = key.lower()
        icon = 'fas fa-info-circle'
        
        for keyword, icon_class in icons.items():
            if keyword in key_lower:
                icon = icon_class
                break
        
        html += f"""
        <div class="contact-item" data-component="contact-item">
            <div class="contact-icon">
                <i class="{icon}"></i>
            </div>
            <div class="contact-details">
                <h4>{key}</h4>
                <p>{value}</p>
            </div>
        </div>
        """
    return html

def generate_css_content(theme, style):
    base_css = f"""
/* Reset and Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    {theme['fonts']}
    background-color: {theme['colors']['background']};
    color: {theme['colors']['text']};
    line-height: 1.6;
    overflow-x: hidden;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Background Animation */
.bg-animation {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    pointer-events: none;
}}

/* Navigation */
.navbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
    transition: all 0.3s ease;
}}

.nav-brand {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.brand-icon {{
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
}}

.brand-text {{
    font-size: 1.5rem;
    font-weight: 700;
    color: {theme['colors']['primary']};
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.nav-link {{
    text-decoration: none;
    color: {theme['colors']['text']};
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    transition: all 0.3s ease;
    position: relative;
}}

.nav-link:hover,
.nav-link.active {{
    color: {theme['colors']['primary']};
    background: rgba({theme['colors']['primary'].replace('#', '')}, 0.1);
}}

.nav-toggle {{
    display: none;
    flex-direction: column;
    cursor: pointer;
}}

.nav-toggle span {{
    width: 25px;
    height: 3px;
    background: {theme['colors']['primary']};
    margin: 3px 0;
    transition: 0.3s;
}}

/* Hero Section */
.hero {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 120px 0 80px;
    position: relative;
}}

.hero-content {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    width: 100%;
}}

.hero-text {{
    animation: slideInLeft 1s ease-out;
}}

.hero-title {{
    margin-bottom: 2rem;
}}

.title-line {{
    display: block;
    font-size: 1.5rem;
    color: {theme['colors']['secondary']};
    margin-bottom: 0.5rem;
}}

.title-name {{
    display: block;
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}}

.title-role {{
    display: block;
    font-size: 2rem;
    color: {theme['colors']['accent']};
    font-weight: 600;
}}

.hero-description {{
    font-size: 1.2rem;
    color: {theme['colors']['secondary']};
    margin-bottom: 3rem;
    max-width: 500px;
}}

.hero-buttons {{
    display: flex;
    gap: 1.5rem;
}}

.btn {{
    padding: 1rem 2rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}}

.btn-primary {{
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    color: white;
    box-shadow: 0 10px 30px rgba({theme['colors']['primary'].replace('#', '')}, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba({theme['colors']['primary'].replace('#', '')}, 0.4);
}}

.btn-secondary {{
    background: transparent;
    color: {theme['colors']['primary']};
    border: 2px solid {theme['colors']['primary']};
}}

.btn-secondary:hover {{
    background: {theme['colors']['primary']};
    color: white;
    transform: translateY(-3px);
}}

.hero-image {{
    display: flex;
    justify-content: center;
    animation: slideInRight 1s ease-out;
}}

.profile-card {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 30px;
    padding: 3rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}}

.profile-avatar {{
    position: relative;
    margin-bottom: 2rem;
}}

.avatar-inner {{
    width: 150px;
    height: 150px;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: bold;
    color: white;
    margin: 0 auto;
    position: relative;
    z-index: 2;
}}

.avatar-ring {{
    position: absolute;
    top: -10px;
    left: -10px;
    right: -10px;
    bottom: -10px;
    border: 3px solid {theme['colors']['accent']};
    border-radius: 50%;
    animation: rotate 10s linear infinite;
}}

.scroll-indicator {{
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    animation: bounce 2s infinite;
}}

/* Sections */
.section {{
    padding: 100px 0;
    position: relative;
}}

.section-header {{
    text-align: center;
    margin-bottom: 5rem;
}}

.section-title {{
    font-size: 3rem;
    font-weight: 800;
    color: {theme['colors']['primary']};
    margin-bottom: 1rem;
    position: relative;
}}

.section-title::after {{
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['accent']});
    border-radius: 2px;
}}

.section-subtitle {{
    font-size: 1.2rem;
    color: {theme['colors']['secondary']};
}}

/* About Section */
.about-content {{
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}

.about-text h3 {{
    font-size: 2rem;
    color: {theme['colors']['primary']};
    margin-bottom: 2rem;
}}

.about-text p {{
    font-size: 1.1rem;
    color: {theme['colors']['secondary']};
    margin-bottom: 3rem;
    line-height: 1.8;
}}

.about-stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-top: 3rem;
}}

.stat-item {{
    text-align: center;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.stat-number {{
    font-size: 3rem;
    font-weight: 900;
    color: {theme['colors']['primary']};
    margin-bottom: 0.5rem;
}}

.stat-label {{
    font-size: 1.1rem;
    color: {theme['colors']['secondary']};
    font-weight: 600;
}}

/* Timeline */
.timeline {{
    position: relative;
    max-width: 800px;
    margin: 0 auto;
}}

.timeline::before {{
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(to bottom, {theme['colors']['primary']}, {theme['colors']['accent']});
    transform: translateX(-50%);
}}

.timeline-item {{
    position: relative;
    margin-bottom: 4rem;
    width: 50%;
    padding: 0 2rem;
}}

.timeline-item:nth-child(odd) {{
    left: 0;
    text-align: right;
}}

.timeline-item:nth-child(even) {{
    left: 50%;
    text-align: left;
}}

.timeline-marker {{
    position: absolute;
    top: 0;
    width: 20px;
    height: 20px;
    background: {theme['colors']['primary']};
    border-radius: 50%;
    border: 4px solid {theme['colors']['background']};
    box-shadow: 0 0 0 4px {theme['colors']['primary']};
}}

.timeline-item:nth-child(odd) .timeline-marker {{
    right: -10px;
}}

.timeline-item:nth-child(even) .timeline-marker {{
    left: -10px;
}}

.timeline-content {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}}

.timeline-content:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}}

.timeline-date {{
    color: {theme['colors']['accent']};
    font-weight: 600;
    margin-bottom: 1rem;
}}

.timeline-title {{
    font-size: 1.5rem;
    color: {theme['colors']['primary']};
    margin-bottom: 0.5rem;
}}

.timeline-company {{
    color: {theme['colors']['secondary']};
    margin-bottom: 1rem;
}}

.timeline-description {{
    color: {theme['colors']['text']};
    margin-bottom: 1.5rem;
    line-height: 1.6;
}}

.timeline-skills {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.skill-chip {{
    background: {theme['colors']['primary']};
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
}}

/* Projects Grid */
.projects-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}}

.project-card {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}}

.project-card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.2);
}}

.project-image {{
    height: 200px;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    position: relative;
    overflow: hidden;
}}

.project-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all 0.3s ease;
}}

.project-card:hover .project-overlay {{
    opacity: 1;
}}

.project-links {{
    display: flex;
    gap: 1rem;
}}

.project-link {{
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.project-link:hover {{
    background: {theme['colors']['primary']};
    transform: scale(1.1);
}}

.project-content {{
    padding: 2rem;
}}

.project-title {{
    font-size: 1.5rem;
    color: {theme['colors']['primary']};
    margin-bottom: 1rem;
    font-weight: 700;
}}

.project-description {{
    color: {theme['colors']['secondary']};
    margin-bottom: 1.5rem;
    line-height: 1.6;
}}

.project-tech {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.tech-tag {{
    background: rgba({theme['colors']['accent'].replace('#', '')}, 0.2);
    color: {theme['colors']['accent']};
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
}}

/* Skills */
.skills-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}}

.skill-category {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.skill-category-title {{
    font-size: 1.5rem;
    color: {theme['colors']['primary']};
    margin-bottom: 2rem;
    font-weight: 700;
}}

.skill-items {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.skill-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.skill-name {{
    font-weight: 600;
    color: {theme['colors']['text']};
}}

.skill-bar {{
    width: 100px;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
}}

.skill-progress {{
    height: 100%;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['accent']});
    width: 85%;
    border-radius: 4px;
    animation: fillBar 2s ease-out;
}}

/* Education */
.education-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}}

.education-card {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: all 0.3s ease;
}}

.education-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
}}

.education-icon {{
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['accent']});
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
}}

.education-degree {{
    font-size: 1.3rem;
    color: {theme['colors']['primary']};
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

.education-school {{
    color: {theme['colors']['secondary']};
    margin-bottom: 0.5rem;
}}

.education-grade {{
    color: {theme['colors']['accent']};
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.education-year {{
    color: {theme['colors']['text']};
    font-size: 0.9rem;
}}

/* Contact */
.contact-content {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    max-width: 1000px;
    margin: 0 auto;
}}

.contact-info {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.contact-item {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}}

.contact-item:hover {{
    transform: translateX(10px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}}

.contact-icon {{
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, {theme['colors']['primary']}, {theme['colors']['accent']});
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.2rem;
}}

.contact-details h4 {{
    color: {theme['colors']['primary']};
    margin-bottom: 0.5rem;
    font-weight: 600;
}}

.contact-details p {{
    color: {theme['colors']['secondary']};
}}

.contact-form {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.form {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.form-group {{
    position: relative;
}}

.form-input,
.form-textarea {{
    width: 100%;
    padding: 1rem 1.5rem;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid transparent;
    border-radius: 15px;
    color: {theme['colors']['text']};
    font-size: 1rem;
    transition: all 0.3s ease;
}}

.form-input:focus,
.form-textarea:focus {{
    outline: none;
    border-color: {theme['colors']['primary']};
    background: rgba(255, 255, 255, 0.15);
}}

.form-textarea {{
    min-height: 120px;
    resize: vertical;
}}

/* Animations */
@keyframes slideInLeft {{
    from {{
        opacity: 0;
        transform: translateX(-50px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

@keyframes slideInRight {{
    from {{
        opacity: 0;
        transform: translateX(50px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

@keyframes rotate {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{
        transform: translateY(0);
    }}
    40% {{
        transform: translateY(-10px);
    }}
    60% {{
        transform: translateY(-5px);
    }}
}}

@keyframes fillBar {{
    from {{ width: 0; }}
    to {{ width: 85%; }}
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .hero-content {{
        grid-template-columns: 1fr;
        text-align: center;
    }}
    
    .title-name {{
        font-size: 2.5rem;
    }}
    
    .timeline::before {{
        left: 20px;
    }}
    
    .timeline-item {{
        width: 100%;
        left: 0 !important;
        text-align: left !important;
        padding-left: 60px;
    }}
    
    .timeline-marker {{
        left: 10px !important;
    }}
    
    .contact-content {{
        grid-template-columns: 1fr;
        gap: 2rem;
    }}
    
    .nav-links {{
        display: none;
    }}
    
    .nav-toggle {{
        display: flex;
    }}
}}
"""

    # Add style-specific CSS
    if style == "futuristic":
        base_css += f"""
/* Futuristic Specific Styles */
.navbar {{
    background: rgba(10, 10, 10, 0.95);
    border-bottom: 1px solid {theme['colors']['primary']};
}}

.stars {{
    position: absolute;
    width: 100%;
    height: 100%;
    background: transparent;
}}

.stars::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, {theme['colors']['primary']}, transparent),
        radial-gradient(2px 2px at 40px 70px, {theme['colors']['secondary']}, transparent),
        radial-gradient(1px 1px at 90px 40px, {theme['colors']['accent']}, transparent);
    background-repeat: repeat;
    background-size: 200px 100px;
    animation: stars 20s linear infinite;
}}

.particles {{
    position: absolute;
    width: 100%;
    height: 100%;
}}

.particles::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, {theme['colors']['primary']}22, transparent);
    animation: scan 3s linear infinite;
}}

.grid-overlay {{
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient({theme['colors']['primary']}22 1px, transparent 1px),
        linear-gradient(90deg, {theme['colors']['primary']}22 1px, transparent 1px);
    background-size: 50px 50px;
    animation: gridMove 20s linear infinite;
}}

@keyframes stars {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-100px); }}
}}

@keyframes scan {{
    0% {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}

@keyframes gridMove {{
    from {{ transform: translate(0, 0); }}
    to {{ transform: translate(50px, 50px); }}
}}

.section {{
    background: rgba(26, 26, 46, 0.3);
    border: 1px solid {theme['colors']['primary']}33;
}}

.project-card,
.education-card,
.contact-item,
.timeline-content {{
    box-shadow: 0 0 20px {theme['colors']['primary']}33;
}}

.project-card:hover,
.education-card:hover,
.contact-item:hover,
.timeline-content:hover {{
    box-shadow: 0 0 40px {theme['colors']['primary']}66;
}}
"""
    elif style == "playful":
        base_css += f"""
/* Playful Specific Styles */
.floating-shapes {{
    position: absolute;
    width: 100%;
    height: 100%;
}}

.shape {{
    position: absolute;
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}}

.shape-1 {{
    width: 80px;
    height: 80px;
    background: linear-gradient(45deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    top: 20%;
    left: 10%;
    animation-delay: 0s;
}}

.shape-2 {{
    width: 60px;
    height: 60px;
    background: linear-gradient(45deg, {theme['colors']['secondary']}, {theme['colors']['accent']});
    top: 60%;
    right: 20%;
    animation-delay: 2s;
}}

.shape-3 {{
    width: 100px;
    height: 100px;
    background: linear-gradient(45deg, {theme['colors']['accent']}, {theme['colors']['primary']});
    bottom: 30%;
    left: 20%;
    animation-delay: 4s;
}}

.shape-4 {{
    width: 40px;
    height: 40px;
    background: linear-gradient(45deg, {theme['colors']['primary']}, {theme['colors']['accent']});
    top: 40%;
    right: 10%;
    animation-delay: 1s;
}}

.shape-5 {{
    width: 70px;
    height: 70px;
    background: linear-gradient(45deg, {theme['colors']['secondary']}, {theme['colors']['primary']});
    bottom: 20%;
    right: 30%;
    animation-delay: 3s;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
    33% {{ transform: translateY(-20px) rotate(120deg); }}
    66% {{ transform: translateY(20px) rotate(240deg); }}
}}

.project-card:hover {{
    animation: wiggle 0.5s ease-in-out;
}}

.skill-item:hover {{
    animation: bounce 0.6s ease-in-out;
}}

@keyframes wiggle {{
    0%, 100% {{ transform: rotate(0deg); }}
    25% {{ transform: rotate(-3deg); }}
    75% {{ transform: rotate(3deg); }}
}}

.btn:hover {{
    animation: pulse 0.6s ease-in-out;
}}

@keyframes pulse {{
    0% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
    100% {{ transform: scale(1); }}
}}
"""
    else:  # professional
        base_css += f"""
/* Professional Specific Styles */
.gradient-orbs {{
    position: absolute;
    width: 100%;
    height: 100%;
}}

.orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.3;
    animation: drift 20s ease-in-out infinite;
}}

.orb-1 {{
    width: 300px;
    height: 300px;
    background: linear-gradient(45deg, {theme['colors']['primary']}, {theme['colors']['secondary']});
    top: 20%;
    left: 10%;
    animation-delay: 0s;
}}

.orb-2 {{
    width: 200px;
    height: 200px;
    background: linear-gradient(45deg, {theme['colors']['secondary']}, {theme['colors']['accent']});
    top: 60%;
    right: 20%;
    animation-delay: 7s;
}}

.orb-3 {{
    width: 250px;
    height: 250px;
    background: linear-gradient(45deg, {theme['colors']['accent']}, {theme['colors']['primary']});
    bottom: 30%;
    left: 30%;
    animation-delay: 14s;
}}

@keyframes drift {{
    0%, 100% {{ transform: translate(0, 0) scale(1); }}
    33% {{ transform: translate(30px, -30px) scale(1.1); }}
    66% {{ transform: translate(-20px, 20px) scale(0.9); }}
}}

.section:nth-child(even) {{
    background: rgba(248, 250, 252, 0.5);
}}
"""

    return base_css

def generate_js_content(style):
    base_js = """
// BULLETPROOF COMPONENT SELECTION SYSTEM - FINAL FIX
console.log('Loading BULLETPROOF editing system with persistent component references...');

// Enhanced global state with persistent component tracking
window.EditingSystem = {
    selectedComponent: null,
    selectedComponentData: null, // Store component data separately
    editPanel: null,
    isEditPanelOpen: false,
    editingInitialized: false,
    componentRegistry: new Map(),
    // Add backup reference system
    lastSelectedComponent: null,
    componentSelectionTime: null
};

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log(' DOM loaded - initializing BULLETPROOF systems...');
    
    initializeNavigation();
    initializeAnimations();
    initializeEditingSystem();
    
    console.log('All systems initialized successfully');
});

function initializeNavigation() {
    console.log(' Initializing navigation...');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section, .hero');
    
    // Smooth scrolling
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Active navigation highlighting
    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
    
    console.log('Navigation initialized');
}

function initializeAnimations() {
    console.log('Initializing animations...');
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.section, .project-card, .education-card, .timeline-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Skill bars animation
    const skillBars = document.querySelectorAll('.skill-progress');
    const skillObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.width = '85%';
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => {
        bar.style.width = '0%';
        bar.style.transition = 'width 2s ease';
        skillObserver.observe(bar);
    });
    
    console.log('Animations initialized');
}



function setupEnhancedGlobalEventHandlers() {
    console.log('Setting up enhanced global event handlers...');
    
    // Global click handler with enhanced protection
    document.addEventListener('click', function(e) {
        // Don't close if clicking inside the edit panel
        if (window.EditingSystem.editPanel && window.EditingSystem.editPanel.contains(e.target)) {
            console.log('Click inside edit panel - maintaining selection');
            return;
        }
        
        // Don't close if clicking on an editable component
        if (e.target.closest('[data-component]')) {
            console.log('Click on editable component - maintaining selection');
            return;
        }
        
        // Only close if we're clicking outside everything and panel is open
        if (window.EditingSystem.isEditPanelOpen) {
            console.log('Closing edit panel due to outside click');
            closeEditPanelSafely();
        }
    });
    
    // Escape key handler
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && window.EditingSystem.isEditPanelOpen) {
            console.log('Closing edit panel due to Escape key');
            closeEditPanelSafely();
        }
    });
    
    console.log('Enhanced global event handlers setup complete');
}


function setupSingleComponentWithPersistence(component) {
    console.log(`Setting up single component with persistence: ${component.dataset.component}`);
    
    // Generate unique ID
    const componentId = `edit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    component.setAttribute('data-edit-id', componentId);
    
    // Store comprehensive data in registry
    const componentData = {
        element: component,
        type: component.dataset.component,
        originalHTML: component.outerHTML,
        id: componentId,
        timestamp: Date.now()
    };
    
    window.EditingSystem.componentRegistry.set(componentId, componentData);
    
    // Setup visual indicators
    component.style.cursor = 'pointer';
    component.title = `Click to edit: ${component.dataset.component}`;
    
    // Add event listeners with persistence
    component.addEventListener('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        console.log(`Component clicked: ${this.dataset.component} (ID: ${componentId})`);
        selectComponentForEditingWithPersistence(this, componentId, componentData);
    });
    
    component.addEventListener('mouseenter', function() {
        if (window.EditingSystem.selectedComponent !== this) {
            this.classList.add('hover-editable');
        }
    });
    
    component.addEventListener('mouseleave', function() {
        this.classList.remove('hover-editable');
    });
    
    console.log(`Single component setup with persistence complete: ${component.dataset.component}`);
}

function formatComponentName(componentName) {
    return componentName
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function showStatus(message, type) {
    const statusDiv = document.querySelector('.edit-panel-status');
    if (statusDiv) {
        statusDiv.innerHTML = `<div class="status-message status-${type}">${message}</div>`;
    }
    console.log(`Status: ${message} (${type})`);
}

function showNotification(message, type) {
    console.log(`Notification: ${message} (${type})`);
    
    // Remove existing notifications
    document.querySelectorAll('.notification').forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" type="button">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Add close listener
    notification.querySelector('.notification-close').addEventListener('click', function() {
        notification.remove();
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Form submission handler
document.addEventListener('submit', function(e) {
    if (e.target.classList.contains('form')) {
        e.preventDefault();
        showNotification('Thank you for your message! I will get back to you soon.', 'success');
        e.target.reset();
    }
});

console.log(' BULLETPROOF EDITING SYSTEM WITH PERSISTENCE LOADED SUCCESSFULLY!');
console.log('Debug commands: debugEditingSystemFull(), testComponentSelectionPersistence()');
console.log('Backend: GROQ AI for component modifications');
console.log('Persistence: Multiple reference system with recovery mechanisms');
"""

    return base_js

app = Flask(__name__)
CORS(app, origins=["https://launchmyfolio.vercel.app/"])

# Create directories
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated_websites'
for folder in [UPLOAD_FOLDER, GENERATED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Resume parser with GROQ is running'})

@app.route('/test-groq', methods=['GET'])
def test_groq():
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'GROQ AI is working correctly!'"}],
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        return jsonify({
            'success': True,
            'message': response.choices[0].message.content.strip()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400

        # Save and process file
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            file.save(filepath)
            
            # Extract text from PDF
            with pdfplumber.open(filepath) as pdf:
                content = pdf.pages[0].extract_text()
            
            if not content:
                return jsonify({'error': 'Could not extract text from PDF'}), 400
            
            # Parse with GROQ
            info = get_all_info(content)
            
            # Convert to dict for website generation
            data = {
                "name": info.name,
                "job_title": info.job_title,
                "hero_description": info.hero_description,  # NEW
                "about_description": info.about_description,  # NEW
                "education": [{"Institute_name": edu.Institute_name, "Degree_name": edu.Degree_name, "Marks": edu.marks, "start_date" : edu.start_time, "end_date": edu.end_time} for edu in info.Education],
                "Contact_Info": info.Contact_Info,
                "skills": info.Skills,
                "projects": [{"title": p.project_name, "desc": p.about_project, "tech": p.skills_used} for p in info.Projects],
                "Experience": [{"Company": exp.Company_name, "Position": exp.Position_name, "Skills": exp.skills_used, "start_date" : exp.start_date, "end_date" : exp.end_date} for exp in info.Experience],
                "Achievements": [{"achievement_name": a.Achivement_name, "institute_name": a.institute_name, "description": a.about} for a in info.Achivements],
                "Position_of_responsibility": [{"position_name": p.Position_name, "soc_name": p.Society_name, "description": p.Description} for p in info.Position_of_Responsibility]
            }
            
            return jsonify({
                'success': True,
                'data': data,
                'message': 'Resume parsed successfully'
            })
            
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Failed to process resume: {str(e)}'}), 500

@app.route('/generate-website', methods=['POST'])
def generate_website():
    try:
        request_data = request.get_json()
        resume_data = request_data.get('data')
        style = request_data.get('style', 'professional')
        
        if not resume_data:
            return jsonify({'error': 'No resume data provided'}), 400
        
        # Generate website code
        website_code = generate_website_code(resume_data, style)
        
        # Create unique folder for this website
        website_id = str(uuid.uuid4())
        website_folder = os.path.join(app.config['GENERATED_FOLDER'], website_id)
        os.makedirs(website_folder)
        
        # Save files
        with open(os.path.join(website_folder, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(website_code['html'])
        
        with open(os.path.join(website_folder, 'styles.css'), 'w', encoding='utf-8') as f:
            f.write(website_code['css'])
        
        with open(os.path.join(website_folder, 'script.js'), 'w', encoding='utf-8') as f:
            f.write(website_code['js'])
        
        return jsonify({
            'success': True,
            'website_id': website_id,
            'preview_url': f'/preview/{website_id}',
            'download_url': f'/download/{website_id}'
        })
        
    except Exception as e:
        print(f"Error generating website: {str(e)}")
        return jsonify({'error': f'Failed to generate website: {str(e)}'}), 500

@app.route('/preview/<website_id>')
def preview_website(website_id):
    try:
        print(f"Preview request for website ID: {website_id}")
        website_folder = os.path.join(app.config['GENERATED_FOLDER'], website_id)
        index_path = os.path.join(website_folder, 'index.html')
        
        if not os.path.exists(index_path):
            print(f" Website not found: {index_path}")
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Website Not Found</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
                    .error {{ color: #dc2626; }}
                </style>
            </head>
            <body>
                <h1 class="error">Website Not Found</h1>
                <p>Website ID: {website_id}</p>
                <p>The requested website could not be found.</p>
            </body>
            </html>
            """, 404
        
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        print(f"Successfully loaded HTML, length: {len(html_content)}")
        
        response = app.make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        return response
            
    except Exception as e:
        print(f"Error in preview_website: {str(e)}")
        
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Preview Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
                .error {{ color: #dc2626; }}
            </style>
        </head>
        <body>
            <h1 class="error">Preview Error</h1>
            <p>Website ID: {website_id}</p>
            <p>Error: {str(e)}</p>
        </body>
        </html>
        """
        
        response = app.make_response(error_html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response, 500

@app.route('/download/<website_id>')
def download_website(website_id):
    try:
        website_folder = os.path.join(app.config['GENERATED_FOLDER'], website_id)
        
        if not os.path.exists(website_folder):
            return jsonify({'error': 'Website not found'}), 404
        
        # Create zip file
        zip_path = os.path.join(tempfile.gettempdir(), f'portfolio_{website_id}.zip')
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_name in ['index.html', 'styles.css', 'script.js']:
                file_path = os.path.join(website_folder, file_name)
                if os.path.exists(file_path):
                    zipf.write(file_path, file_name)
        
        return send_file(zip_path, as_attachment=True, download_name=f'portfolio_website.zip')
        
    except Exception as e:
        return jsonify({'error': f'Failed to create download: {str(e)}'}), 500

# Add these helper functions above generate_website_code:
def generate_hero_description(data):
    job_title = data.get('job_title', 'professional').lower()
    skills = data.get('skills', [])
    experience_count = len(data.get('Experience', []))
    if skills:
        top_skills = ', '.join(skills[:3])
        desc = f"Experienced {job_title} skilled in {top_skills}. Passionate about building impactful digital solutions."
    else:
        desc = f"Experienced {job_title} passionate about building impactful digital solutions."
    if experience_count > 0:
        desc += f" {experience_count} years of experience."
    return desc

def generate_about_description(data):
    job_title = data.get('job_title', 'professional').lower()
    skills = data.get('skills', [])
    experience_count = len(data.get('Experience', []))
    projects_count = len(data.get('projects', []))
    if skills:
        top_skills = ', '.join(skills[:3])
        description = f"I'm a {job_title} with expertise in {top_skills}. "
    else:
        description = f"I'm a {job_title} with a strong foundation in technology. "
    if experience_count > 0:
        description += f"With {experience_count} years of professional experience, "
    description += "I specialize in creating innovative solutions and delivering exceptional results. "
    if projects_count > 0:
        description += f"I've completed {projects_count} projects, demonstrating my ability to tackle complex challenges and deliver high-quality outcomes."
    else:
        description += "I bring ideas to life through clean code and innovative solutions."
    return description

if __name__ == '__main__':
    print("\n" + "="*60)
    print("BULLETPROOF PORTFOLIO GENERATOR WITH GROQ AI")
    print("="*60)
    print(f"GROQ API configured: {'Yes' if groq_api_key else 'No'}")
    print(f"AI Backend: GROQ (llama-3.3-70b-versatile)")
    print(f"Component Selection: Bulletproof with persistence")
    print(f" Upload folder: {UPLOAD_FOLDER}")
    print(f" Generated websites folder: {GENERATED_FOLDER}")
    print("="*60)
    print("Available endpoints:")
    print("  POST / - Upload and parse resume")
    print("   POST /generate-website - Generate portfolio website")
    print("  POST /modify-component - Modify component with GROQ AI")
    print("   GET /preview/<id> - Preview generated website")
    print("  GET /download/<id> - Download website files")
    print("   GET /health - Health check")
    print("   GET /test-groq - Test GROQ AI connection")
    print("="*60)
    print(" Debug Features:")
    print("  Frontend: debugEditingSystemFull()")
    print(" Frontend: testComponentSelectionPersistence()")
    print(" Backend: Comprehensive request/response logging")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
