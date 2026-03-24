---
layout: default
title: Classic Spaghetti Bolognese Implementation
---

# Classic Spaghetti Bolognese Implementation

This documentation provides a standardized procedure for preparing a high-quality spaghetti bolognese, focusing on ingredient preparation, heat management, and assembly techniques.

## 1. Component Specifications

### 1.1 Ingredients (YAML Configuration)
```yaml
ingredients:
  pasta:
    type: spaghetti
    amount: 500g
  protein:
    type: ground_beef
    fat_content: 20%
    amount: 500g
  aromatics:
    onion: 1 large
    garlic: 3 cloves
  sauce_base:
    crushed_tomatoes: 800g
    tomato_paste: 2 tbsp
  seasoning:
    oregano: 1 tsp
    salt: to_taste
    pepper: to_taste
```

### 1.2 Required Hardware
- Large stockpot (minimum 5L capacity)
- Heavy-bottomed skillet or Dutch oven
- Colander for drainage

## 2. Step-by-Step Execution

### 2.1 Base Layer Initialization
Begin by heating 2 tablespoons of extra virgin olive oil in your skillet over medium-high heat. Add the finely diced onion and sauté until the onions reach a translucent state (approximately 5 minutes). Add minced garlic and cook for an additional 60 seconds to avoid burning.

### 2.2 Protein Processing
Add the ground beef to the skillet. Increase heat slightly to ensure browning rather than steaming. Use a spatula to break the meat into small, uniform granules. Cook until no pink remains.

### 2.3 Sauce Synthesis
1. **Integration:** Stir in the tomato paste and cook for 2 minutes to caramelize the sugars.
2. **Hydration:** Add the crushed tomatoes and seasonings.
3. **Simmering:** Reduce heat to low. Allow the sauce to simmer for 30 minutes. This duration is critical for flavor development. You can monitor the process with a simple timer:
```bash
sleep 1800 && echo "Sauce reduction complete"
```

## 3. Final Assembly and Serving

### 3.1 Pasta Boiling
Bring a large pot of water to a rolling boil. Add 1 tablespoon of salt. Submerge the spaghetti and cook according to package instructions until the texture is *al dente* (firm to the bite). 

### 3.2 Drainage and Plating
Drain the pasta using the colander. Do not rinse the pasta, as the surface starches are necessary for sauce adhesion. Combine the pasta and sauce in the skillet or plate individually. Top with grated Parmesan for optimal results.

---
**Source:** [GitHub Issue #11](https://github.com/coltonchrane/TechNotes/issues/11) | **Contributor:** @coltonchrane