from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

def create_star_rating_svg(rating):
    """Create an SVG star rating display.
    
    Args:
        rating (float): Rating value between 0 and 5
        
    Returns:
        str: SVG string showing filled and empty stars
    """
    # Clamp rating between 0 and 5
    rating = max(0, min(5, rating))
    
    # Calculate full and partial stars
    full_stars = int(rating)
    partial = rating - full_stars
    empty_stars = 5 - full_stars - (1 if partial > 0 else 0)

    svg = '''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 24">
    '''
    
    # Add full stars
    for i in range(full_stars):
        x = i * 24
        svg += f'''
        <path transform="translate({x},0)" fill="gold" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
        '''
    
    # Add partial star if needed
    if partial > 0:
        x = full_stars * 24
        svg += f'''
        <defs>
            <clipPath id="partial">
                <rect x="0" y="0" width="{partial * 24}" height="24" />
            </clipPath>
        </defs>
        <path transform="translate({x},0)" fill="#ddd" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
        <path transform="translate({x},0)" fill="gold" clip-path="url(#partial)" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
        '''
    
    # Add empty stars
    for i in range(empty_stars):
        x = (full_stars + (1 if partial > 0 else 0) + i) * 24
        svg += f'''
        <path transform="translate({x},0)" fill="#ddd" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
        '''
    
    svg += '</svg>'
    return svg

@app.route("/<float:rating>/")
def get_star_rating_svg(rating):
    """Route to generate star rating SVG.
    
    Args:
        rating (float): Rating value between 0 and 5
        
    Returns:
        Response: SVG image response
    """
    svg = create_star_rating_svg(rating)
    response = make_response(svg)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


@app.route("/")
def redirect_to_github():
    return redirect("https://github.com/goulartnogueira/starrating", code=302)

if __name__ == "__main__":
    app.run()
