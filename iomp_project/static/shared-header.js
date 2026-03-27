// Shared Header Component - Universal Navigation
// Works across all modules with absolute URLs

document.write(`
<header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div class="logo">
            <h1 style="font-size: 2rem; font-weight: 700; margin: 0;">🪙 AI-Powered Currency Analyzer</h1>
        </div>
        <nav>
            <ul style="list-style: none; display: flex; gap: 20px; margin: 0; padding: 0; flex-wrap: wrap;">
                <li><a href="http://127.0.0.1:5000/home" style="color: white; text-decoration: none; font-weight: 600; padding: 8px 15px; border-radius: 5px; transition: all 0.3s ease;">Home</a></li>
                <li><a href="http://127.0.0.1:5000/home/aboutus.html" style="color: white; text-decoration: none; font-weight: 600; padding: 8px 15px; border-radius: 5px; transition: all 0.3s ease;">About Us</a></li>
                <li><a href="http://127.0.0.1:5000" style="color: white; text-decoration: none; font-weight: 600; padding: 8px 15px; border-radius: 5px; transition: all 0.3s ease;">Conversion</a></li>
                <li><a href="http://127.0.0.1:5001" style="color: white; text-decoration: none; font-weight: 600; padding: 8px 15px; border-radius: 5px; transition: all 0.3s ease;">Education</a></li>
                <li><a href="http://127.0.0.1:5000/home/contactus.html" style="color: white; text-decoration: none; font-weight: 600; padding: 8px 15px; border-radius: 5px; transition: all 0.3s ease;">Contact Us</a></li>
            </ul>
        </nav>
    </div>
</header>
`);

// Add hover effects and responsive styles
const style = document.createElement('style');
style.textContent = `
    header nav a:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    @media (max-width: 768px) {
        header h1 { 
            font-size: 1.5rem !important; 
        }
        header nav ul { 
            gap: 10px !important; 
            justify-content: center; 
        }
        header > div { 
            flex-direction: column !important; 
            text-align: center; 
        }
    }
`;
document.head.appendChild(style);