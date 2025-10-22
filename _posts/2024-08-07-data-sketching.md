---
title: "Data Sketching: The Art of Guesstimating with Big Data"
date: 2024-08-07 7:45:00 -0500
categories:
  - dataengineering
  - datavisualization
  - datasketching
  - datasketch
author: steven
---

# Data Sketching: The Art of Guesstimating with Big Data

Picture this: You're at a county fair, and there's a huge jar of jellybeans. The person who guesses closest to the actual number wins a
prize. Now, you could try counting each jellybean individually, but that would take forever. Instead, you might estimate based on the jar's
size, how densely packed the beans are, and maybe a quick count of one small section. That's essentially what data sketching does, but for
massive datasets.

## What is Data Sketching?

Data sketching is like being a clever detective with big data. Instead of examining every single piece of evidence (which could take years),
you use smart techniques to get a good idea of what's going on without looking at everything. It's all about making educated guesses that
are "good enough" for practical purposes.

The beauty of data sketching is that it lets you work with enormous amounts of data using limited memory and processing power. It's like
summarizing a thousand-page novel in a few paragraphs - you lose some details, but you capture the essence.

## Aspects of Data Sketching

1. **One-Pass Processing**: Data sketching algorithms typically only need to see each data point once. This is crucial when dealing with
   streaming data or datasets too large to fit in memory.

2. **Approximate Results**: Sketches provide estimates, not exact answers. But these estimates often come with provable error bounds, so you
   know how much to trust them.

3. **Space Efficiency**: Sketches use way less memory than the full dataset. It's like compressing a high-res photo into a smaller file -
   you lose some quality, but it's much easier to store and share.

4. **Fast Processing**: Because sketches are small and approximate, computations on them are typically very fast.

## Data Sketching Techniques and When to Use Them

### Counting and Frequency Estimation
- **Count-Min Sketch**:
  - What it does: Estimates how often items appear in a data stream.
  - When to use it: Tracking trending hashtags on social media or popular products in e-commerce.

- **HyperLogLog**:
  - What it does: Estimates the number of unique elements (cardinality) in a dataset.
  - When to use it: Counting unique visitors to a website or unique products in a large inventory.

### Set Operations
**Bloom Filters**:
- What it does: Tests whether an element is a member of a set.
- When to use it: Checking if a username already exists or if an email is in a spam database.

### Quantiles and Rankings
**T-Digest**:
- What it does: Estimates percentiles and creates histograms.
- When to use it: Analyzing response times in a web service or summarizing large datasets of numerical values.

### Sampling
**Reservoir Sampling**:
  - What it does: Maintains a random sample of items from a data stream.
  - When to use it: Keeping a representative sample of user actions on a busy website.

## Data Sketching in Python with Visualizations
In Python, the `datasketch` library is a popular choice for data sketching. Let's look at some examples and create some impressive
visualizations.

### HyperLogLog for Cardinality Estimation

First, let's use HyperLogLog to estimate unique visitors to a website:

```python
import numpy as np
import matplotlib.pyplot as plt
from datasketch import HyperLogLog


def simulate_website_traffic(n_days, n_visitors_per_day):
  hll = HyperLogLog()
  true_uniques = set()
  estimated_uniques = []
  true_uniques_count = []

  for _ in range(n_days):
    daily_visitors = np.random.randint(0, n_visitors_per_day * 10, n_visitors_per_day)
    for visitor in daily_visitors:
      hll.update(str(visitor).encode('utf8'))
      true_uniques.add(visitor)
    estimated_uniques.append(len(hll))
    true_uniques_count.append(len(true_uniques))

  return estimated_uniques, true_uniques_count


# Simulate 30 days of traffic
n_days = 30
n_visitors_per_day = 10000
estimated, true = simulate_website_traffic(n_days, n_visitors_per_day)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(range(1, n_days + 1), true, label='True Uniques', marker='o')
plt.plot(range(1, n_days + 1), estimated, label='HyperLogLog Estimate', marker='x')
plt.title('Website Unique Visitors: True vs HyperLogLog Estimate')
plt.xlabel('Days')
plt.ylabel('Unique Visitors')
plt.legend()
plt.grid(True)
plt.show()
```

This code simulates website traffic and compares the true number of unique visitors with the HyperLogLog estimate. The resulting plot shows
how accurate the estimation is over time.

### Count-Min Sketch for Frequency Estimation

Now, let's use Count-Min Sketch to estimate word frequencies in a large text:

```python
import numpy as np
import matplotlib.pyplot as plt
from countminsketch import CountMinSketch


def generate_word_stream(n_words, vocabulary_size):
  return np.random.randint(0, vocabulary_size, n_words)


# Generate a stream of words
n_words = 1000000
vocabulary_size = 1000
word_stream = generate_word_stream(n_words, vocabulary_size)

# Use Count-Min Sketch
cms = CountMinSketch(width=1000, depth=10)
for word in word_stream:
  cms.add(word)

# Get true frequencies
true_freq = np.bincount(word_stream)

# Get estimated frequencies
estimated_freq = [cms.check(i) for i in range(vocabulary_size)]

# Plot results
plt.figure(figsize=(12, 6))
plt.scatter(true_freq, estimated_freq, alpha=0.5)
plt.plot([0, max(true_freq)], [0, max(true_freq)], 'r--')  # Perfect estimation line
plt.title('Word Frequency: True vs Count-Min Sketch Estimate')
plt.xlabel('True Frequency')
plt.ylabel('Estimated Frequency')
plt.grid(True)
plt.show()
```

This code generates a stream of "words" (represented by integers) and uses Count-Min Sketch to estimate their frequencies. The scatter plot
compares true frequencies with estimated frequencies.

These visualizations demonstrate the power of data sketching techniques. They allow us to process and analyze enormous amounts of data
efficiently, providing useful insights without the need to store or process every single data point.

Remember, data sketching is all about making smart trade-offs. You're exchanging a bit of accuracy for a lot of speed and efficiency. It's
not about getting perfect answers, but about getting useful insights from data that would otherwise be too big to handle.

So next time you're faced with a dataset as big as that jellybean jar at the county fair, don't panic! Reach for a data sketch, and you'll
be making educated guesses in no time.