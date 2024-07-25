import re
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Define keywords for styles
style_keywords = {
    "Modern": ["sleek", "contemporary", "minimalist", "clean lines", "chic", "streamlined", "functional", "geometric", "urban", "stylish", "innovative", "high-tech", "bold"],
    "Traditional": ["classic", "vintage", "ornate", "elegant", "timeless", "decorative", "antique", "detailed", "rich", "grand", "heritage", "refined"],
    "Scandinavian": ["simple", "functional", "natural materials", "light", "cozy", "clean", "bright", "warm", "rustic", "minimalist", "inviting", "clutter-free"],
    "Contemporary": ["current", "trendy", "cutting-edge", "stylish", "innovative", "high-end", "sleek", "fresh", "eclectic", "polished", "updated", "vibrant"],
    "Bohemian": ["eclectic", "artistic", "free-spirited", "colorful", "vintage", "layered", "textured", "cozy", "natural", "exotic", "creative", "casual"],
    "Minimalist": ["simple", "clean", "uncluttered", "sparse", "functional", "neutral", "essential", "sleek", "monochrome", "efficient", "space-saving", "elegant"],
    "Transitional": ["blend", "mix", "modern meets traditional", "neutral", "balanced", "comfortable", "classic with a twist", "warm tones", "updated", "stylish", "subtle", "versatile"],
}

# Function to classify style based on keywords
def classify_style(description):
    style_scores = {style: 0 for style in style_keywords}
    
    # Tokenize and normalize the description
    words = re.findall(r'\b\w+\b', description.lower())
    
    for style, keywords in style_keywords.items():
        for keyword in keywords:
            if keyword in description.lower():
                style_scores[style] += 1
    
    # Determine the style with the highest score
    best_style = max(style_scores, key=style_scores.get)
    return best_style

df = pd.read_csv('furniture_data.csv')
descriptions = df['Description']

styles = []

# Classify each description
for desc in descriptions:
    styles.append(classify_style(desc))

df['Style'] = styles

df.to_csv('styles.csv', index=False)

for index, row in df.iterrows():
    im_path = row.loc['Image Path']
    style = row.loc['Style']
    
    img = Image.open(im_path)
    img_array = np.array(img)   

    plt.imshow(img_array)
    plt.axis('off')
    plt.title(style)
    plt.show()