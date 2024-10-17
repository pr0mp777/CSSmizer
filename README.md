# CSSmizer

![image](https://github.com/user-attachments/assets/e52587c3-b900-4402-ae5f-ac20170f2fe9)

## A Simple Tool for CSS Optimization

**CSSmizer** is a command-line tool I created to help optimize my CSS files and streamline my workflow. It reduces file sizes and improves loading speeds, making my daily web development tasks easier.

### Features

- Combine multiple CSS files into one optimized file.
- Minify CSS by removing unnecessary spaces and comments.
- Fast processing to quickly get the optimized output.

### Requirements

- Python 3.x
- `rich` library

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/xPr0mp7x/CSSmizer.git
    ```

2. Navigate to the project directory:

    ```bash
    cd CSSmizer
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    
### Usage

Run CSSmizer from the command line with one or more CSS files as arguments. The optimized files will be saved in the same directory.

#### Optimize a Single CSS File

To optimize `test1.css`, run:

```bash
python cssmizer.py path/to/test1.css
```

#### Combine and Optimize Multiple CSS Files

To optimize and combine `test1.css` and `test2.css`, run:

```bash
python cssmizer.py path/to/test1.css path/to/test2.css
```

### Example Files

You can find example CSS files in the repository.

### Contributing

If you have suggestions for improvements or find any issues, feel free to open an issue or submit a pull request! Your contributions are welcome and appreciated.

### Note

I developed this tool to simplify my daily CSS workflow. If you find it helpful, please give it a star...!
