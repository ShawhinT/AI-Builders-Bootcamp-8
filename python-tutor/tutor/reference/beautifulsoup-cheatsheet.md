# BeautifulSoup Cheatsheet

Quick reference for the BS4 patterns used in your `example.ipynb` job scraper.

---

## Creating a Soup Object

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_string, "html.parser")
```

**What it does:** Converts raw HTML text into a searchable object
**Where you use it:** `example.ipynb` line 10 (in loop), and in `extract_job_data()` function

---

## Finding Elements

### `find()` - Get First Match

```python
title = soup.find("h1")
company = soup.find("p", class_="company-name")
```

**What it does:** Returns the **first** element that matches
**Returns:** A single tag object (or `None` if not found)
**Where you use it:** `extract_job_data()` function throughout

**Example from your code:**
```python
# example.ipynb, extract_job_data() function
title = soup.find("h1")
```

---

### `find_all()` - Get All Matches

```python
all_links = soup.find_all("a")
job_cards = soup.find_all("a", class_="jobcardStyle1")
```

**What it does:** Returns **all** elements that match
**Returns:** A list of tag objects (empty list `[]` if none found)
**Where you use it:** `example.ipynb` line 13

**Example from your code:**
```python
# example.ipynb, line 13
job_cards = soup.find_all("a", class_="jobcardStyle1")
```

---

### `select_one()` - CSS Selector (First Match)

```python
title = soup.select_one(".post-main-title2")
org = soup.select_one(".post-info2 a p span:last-child")
```

**What it does:** Uses CSS selector syntax (like in stylesheets), returns first match
**Returns:** A single tag object (or `None` if not found)
**Where you use it:** `extract_job_data()` function for fallback searches

**CSS selector patterns:**
- `.classname` - finds by class
- `tag.classname` - finds specific tag with class
- `parent child` - finds child inside parent
- `:last-child` - gets the last child element

---

### `find()` with Text Search

```python
label = soup.find(string=re.compile(r"Job Type", re.I))
```

**What it does:** Finds elements containing specific text (can use regex)
**Where you use it:** `extract_job_data()` when looking for labels like "Location" or "Job Type"

**Example from your code:**
```python
# extract_job_data() function
loc_block = soup.find(string=re.compile(r"Location", re.I))
```

---

## Getting Data from Elements

### `.text` or `.get_text()` - Extract Text

```python
title = soup.find("h1")
print(title.text)           # "Software Engineer"
print(title.get_text())     # "Software Engineer" (same thing)

# With options:
text = element.get_text(" ", strip=True)  # Spaces between parts, remove extra whitespace
```

**What it does:** Gets just the readable text, no HTML tags
**Where you use it:** Throughout `extract_job_data()` function

---

### `tag["attribute"]` - Get Attribute Value

```python
link = soup.find("a")
url = link["href"]           # Get the URL
class_name = link["class"]   # Get the class
```

**What it does:** Extracts attribute values (like dictionary lookup)
**Where you use it:** `example.ipynb` line 13 to get `href` from job links

**Example from your code:**
```python
# example.ipynb, line 13
job_urls_temp = sorted({a["href"] for a in job_cards if a.get("href")})
```

---

### `.get("attribute")` - Safely Get Attribute

```python
url = link.get("href")       # Returns None if href doesn't exist
url = link.get("href", "")   # Returns "" if href doesn't exist
```

**What it does:** Like `tag["attr"]` but won't crash if attribute is missing
**Where you use it:** Throughout `extract_job_data()` when attributes might not exist

---

## Navigating the HTML Tree

### `.find_parent()` - Go Up to Parent

```python
label = soup.find(string="Location")
container = label.find_parent()  # Gets the tag wrapping "Location"
```

**What it does:** Moves up one level in the HTML structure
**Where you use it:** `extract_job_data()` when finding related elements near a label

**Example from your code:**
```python
# extract_job_data() function
lab = soup.find(string=re.compile(r"Location", re.I))
sibp = lab.find_parent().find_next("p")
```

---

### `.find_next()` - Go to Next Sibling

```python
label = soup.find(string="Salary")
value = label.find_parent().find_next("span")  # Gets the next <span> tag
```

**What it does:** Finds the next element at the same level
**Where you use it:** `extract_job_data()` to find values next to labels

---

## Common Patterns in Your Code

### Pattern 1: Check if Element Exists Before Using

```python
title = soup.find("h1")
if title:
    print(title.text)
else:
    print("No title found")
```

**Why:** `find()` returns `None` if nothing matches, which crashes if you try `.text`

---

### Pattern 2: Looping Through Multiple Elements

```python
all_paragraphs = soup.find_all("p")
for p in all_paragraphs:
    print(p.text)
```

**Example from your code:**
```python
# example.ipynb, line 13
for a in job_cards:
    url = a["href"]
```

---

### Pattern 3: Extracting Attributes into a List

```python
job_urls = [a["href"] for a in soup.find_all("a")]
```

**What it does:** List comprehension to grab one attribute from many elements
**Where you use it:** `example.ipynb` line 13

---

### Pattern 4: Fallback Chain (Try Multiple Methods)

```python
title = soup.find("h1")
if not title:
    title = soup.select_one(".job-title")
if not title:
    title = soup.find("span", class_="title-text")

final_title = title.text if title else ""
```

**What it does:** Tries multiple ways to find something (useful when websites vary)
**Where you use it:** `extract_job_data()` function extensively

**Example from your code:**
```python
# extract_job_data() uses first_nonempty() helper to try multiple methods:
title = first_nonempty(
    title,  # From JSON-LD
    text_or_none(soup.select_one(".post-main-title2")),  # CSS selector
    text_or_none(soup.find("h1"))  # Basic find
)
```

---

## Quick Reference Table

| Task | Method | Returns |
|------|--------|---------|
| Find first match | `find("tag")` | Single element or `None` |
| Find all matches | `find_all("tag")` | List of elements |
| Find by class | `find("tag", class_="name")` | Single element or `None` |
| Find by CSS | `select_one(".class")` | Single element or `None` |
| Get text | `.text` or `.get_text()` | String |
| Get attribute | `tag["href"]` | String (crashes if missing) |
| Get attribute safely | `tag.get("href")` | String or `None` |
| Find by text content | `find(string=re.compile("text"))` | String or `None` |
| Go to parent | `.find_parent()` | Element |
| Go to next element | `.find_next()` | Element |

---

## Common Mistakes

### ❌ Wrong: Using .text on None

```python
title = soup.find("h1")
print(title.text)  # Crashes if no <h1> exists!
```

### ✅ Right: Check if element exists first

```python
title = soup.find("h1")
if title:
    print(title.text)
else:
    print("No title found")
```

---

### ❌ Wrong: Using find() when you need all elements

```python
links = soup.find("a")  # Only gets the first link!
```

### ✅ Right: Use find_all() for multiple elements

```python
links = soup.find_all("a")  # Gets all links
```

---

### ❌ Wrong: Accessing missing attributes

```python
link = soup.find("a")
url = link["href"]  # Crashes if href attribute doesn't exist
```

### ✅ Right: Use .get() for optional attributes

```python
link = soup.find("a")
url = link.get("href", "")  # Returns "" if no href
```

---

## Need More Help?

- **Notebook practice:** `tutor/notebooks/html-and-beautifulsoup.ipynb`
- **Your working code:** `example.ipynb` (especially the `extract_job_data()` function)
