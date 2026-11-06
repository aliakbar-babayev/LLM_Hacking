# Visualizations

> Back to [[00_JSMA_Index]] | Previous: [[11_Pairwise_Analysis]]

## Why Visualize?

Visualizations make JSMA results tangible. They show **what** the attack actually does to images and help communicate findings to non-technical audiences.

## Key Visualizations

### 1. Original vs Adversarial Side-by-Side

```python
import matplotlib.pyplot as plt

def plot_comparison(original, adversarial, original_pred, adversarial_pred, confidence_orig, confidence_adv):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # Original
    axes[0].imshow(original.reshape(28, 28), cmap='gray')
    axes[0].set_title(f'Original\nPred: {original_pred} ({confidence_orig:.1%})')
    axes[0].axis('off')
    
    # Adversarial
    axes[1].imshow(adversarial.reshape(28, 28), cmap='gray')
    axes[1].set_title(f'Adversarial\nPred: {adversarial_pred} ({confidence_adv:.1%})')
    axes[1].axis('off')
    
    # Difference (perturbation)
    diff = (adversarial - original).abs().reshape(28, 28)
    axes[2].imshow(diff, cmap='hot')
    axes[2].set_title(f'Perturbation\n({diff.count_nonzero()} pixels)')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('attack_comparison.png', dpi=150)
    plt.show()
```

This shows:
- Left: Original image with correct prediction
- Middle: Adversarial image with wrong prediction
- Right: Heatmap of which pixels changed (bright = modified)

### 2. Saliency Map Visualization

```python
def plot_saliency_map(saliency, title='Saliency Map'):
    plt.figure(figsize=(6, 6))
    
    # Reshape to image dimensions
    saliency_img = saliency.reshape(28, 28)
    
    plt.imshow(saliency_img, cmap='viridis')
    plt.colorbar(label='Saliency Score')
    plt.title(title)
    plt.axis('off')
    plt.savefig('saliency_map.png', dpi=150)
    plt.show()
```

What to look for:
- **Bright spots** = pixels JSMA considers most important
- **Dark areas** = pixels that won't help the attack
- Pattern often aligns with **edges and structural features** of the digit

### 3. Attack Progress Over Iterations

```python
def plot_attack_progress(confidence_history, target_class, source_class):
    """Plot how class confidences change over iterations."""
    iterations = range(len(confidence_history))
    
    plt.figure(figsize=(10, 5))
    
    for class_idx in range(10):
        confidences = [h[class_idx] for h in confidence_history]
        
        if class_idx == target_class:
            plt.plot(iterations, confidences, 'r-', linewidth=2, 
                    label=f'Target (class {class_idx})')
        elif class_idx == source_class:
            plt.plot(iterations, confidences, 'b-', linewidth=2, 
                    label=f'Source (class {class_idx})')
        else:
            plt.plot(iterations, confidences, 'gray', alpha=0.3)
    
    plt.xlabel('Iteration')
    plt.ylabel('Confidence')
    plt.title('Attack Progress: Class Confidences Over Iterations')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('attack_progress.png', dpi=150)
    plt.show()
```

Shows: The **crossover point** where target class confidence exceeds source class.

### 4. Perturbation Heatmap Across Batch

```python
def plot_perturbation_heatmap(perturbation_maps, title='Average Perturbation Map'):
    """Average perturbation across all successful attacks."""
    avg_perturbation = torch.stack(perturbation_maps).mean(dim=0)
    
    plt.figure(figsize=(6, 6))
    plt.imshow(avg_perturbation.reshape(28, 28), cmap='hot')
    plt.colorbar(label='Avg Perturbation')
    plt.title(title)
    plt.axis('off')
    plt.savefig('avg_perturbation.png', dpi=150)
    plt.show()
```

Shows: Which pixel **regions** are consistently targeted across many attacks. Reveals the model's vulnerable features.

### 5. Success Rate Bar Chart

```python
def plot_success_rates(single_results, pairwise_results, classes):
    """Compare single vs pairwise success rates per source class."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    x = range(len(classes))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], single_results, width, label='Single-Pixel')
    ax.bar([i + width/2 for i in x], pairwise_results, width, label='Pairwise')
    
    ax.set_xlabel('Source Class')
    ax.set_ylabel('Success Rate (%)')
    ax.set_title('Attack Success Rate by Source Class')
    ax.set_xticks(x)
    ax.set_xticklabels(classes)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('success_comparison.png', dpi=150)
    plt.show()
```

### 6. Pixel Count Distribution

```python
def plot_pixel_distribution(single_pixels, pairwise_pixels):
    """Histogram of pixels modified for successful attacks."""
    plt.figure(figsize=(8, 5))
    
    plt.hist(single_pixels, bins=20, alpha=0.5, label='Single-Pixel', color='blue')
    plt.hist(pairwise_pixels, bins=20, alpha=0.5, label='Pairwise', color='red')
    
    plt.xlabel('Number of Pixels Modified')
    plt.ylabel('Count')
    plt.title('Distribution of Pixels Modified (Successful Attacks)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('pixel_distribution.png', dpi=150)
    plt.show()
```

## Reading Visualizations — What Matters

| Visualization | Key Insight |
|--------------|-------------|
| Side-by-side | "Can a human tell the difference?" |
| Saliency map | "Where does the model focus?" |
| Attack progress | "How quickly does confidence shift?" |
| Average perturbation | "Which regions are always vulnerable?" |
| Success rate bars | "Which class pairs are weak?" |
| Pixel histogram | "How efficient is the attack?" |

## Key Takeaways

- **Side-by-side** comparisons prove the attack is visually imperceptible
- **Saliency maps** reveal what the model considers important features
- **Progress plots** show the confidence shift over iterations
- **Average perturbation maps** across batches reveal systematic model weaknesses
- Always use visualizations to **communicate results** — numbers alone don't land
