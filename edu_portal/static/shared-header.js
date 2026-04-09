// Shared Header Component - Large Logo Version

document.write(`
<header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div class="logo" style="display: flex; align-items: center; gap: 12px;">
            <img src="https://i.ibb.co/pvZgns3g/Whats-App-Image-2026-04-09-at-6-10-40-PM.jpg"   alt="Currency Analyzer Logo" style="height: 55px; width: auto; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            
            <div>
                <h1 style="font-size: 1.6rem; font-weight: 700; margin: 0; line-height: 1.2;">AI-Powered Currency Analyzer</h1>
                <p style="font-size: 0.85rem; margin: 3px 0 0 0; opacity: 0.9;">Recognition • Conversion • Education</p>
            </div>
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
    
    .logo img {
        transition: all 0.3s ease;
    }
    
    .logo img:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    
    @media (max-width: 768px) {
        header h1 { 
            font-size: 1.3rem !important; 
        }
        
        header p {
            font-size: 0.75rem !important;
        }
        
        header nav ul { 
            gap: 10px !important; 
            justify-content: center; 
        }
        
        header > div { 
            flex-direction: column !important; 
            text-align: center; 
        }
        
        .logo {
            flex-direction: column !important;
        }
        
        .logo img {
            height: 45px !important;
        }
    }
`;
document.head.appendChild(style);