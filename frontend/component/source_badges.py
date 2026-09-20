from urllib.parse import urlparse
import streamlit.components.v1 as components

import streamlit as st


def render_sources(sources: list[str]):
    st.markdown("###### Sources -")
    
    STYLE = """
        display:inline-flex;
        align-items:center;
        gap:6px;
        padding:5px 10px;
        border-radius:999px;
        background:#1f2937;
        color:white;
        border:0.8px solid #374151;
        font-size:11px;
        font-weight:500;
        text-decoration:none;
        """
    
    html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        html, body{
            margin:0;
            padding:0;
            background:transparent;
        }
        </style>
        </head>

        <body>

        <div style="
        display:flex;
        flex-wrap:wrap;
        gap:10px;
        ">
        """ 
    
    for source in sources:
        parsed = urlparse(source)
    
        is_web = parsed.scheme in ("http", "https")
    
        if is_web:
            label = f"🌐 {parsed.netloc.replace('www.', '')}"

            html += f"""
            <a href="{source}" target="_blank"
            style="{STYLE}">
                {label}
            </a>
            """
        else:
            label = f"📄 {source}"

            html += f"""
            <span
            style="{STYLE}; cursor:default;">
                {label}
            </span>
            """
    
    html += "</div>"
    components.html(
        html,
        height = 70 if len(sources) <= 3 else 120,
        scrolling=False,
    )
    