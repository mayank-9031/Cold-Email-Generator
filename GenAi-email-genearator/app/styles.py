def get_css_styles():
    return """
    <style>
        .main {padding: 2rem;}
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            transition: all 0.3s;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        .stDownloadButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 5px !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.3s !important;
            width: 100% !important;
        }
        .stDownloadButton>button:hover {
            background-color: #45a049 !important;
            transform: scale(1.05) !important;
        }
        .email-output {
            padding: 2rem;
            background-color: #f9f9f9;
            border-radius: 10px;
            margin-top: 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
    </style>
    """