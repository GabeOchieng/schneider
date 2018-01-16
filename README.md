3 Energy Efficiency Challenges
==============================

A short description of the competition.

Project Organization
------------

<table>
<thead>
 <tr><th nowrap><code>schneider</code></th><th></th></tr>
</thead>
<tbody>
 <tr>
  <td nowrap><code>├── benchmark</code></td>
  <td>Folder for the benchmark results + blog post notebook.</td>
</tr>
<tr>
  <td nowrap><code>│   └── schneider-benchmark.ipynb</code></td>
  <td>The jupyter notebook to be posted as the benchmark.</td>
</tr>
<tr>
  <td nowrap><code>├── data</code></td>
  <td>Data folder</td>
</tr>
<tr>
  <td nowrap><code>│   ├── final</code></td>
  <td>The data to be used in the competition</td>
</tr>
<tr>
  <td nowrap><code>│   │   ├── private</code></td>
  <td>Data not released to competitors</td>
</tr>
<tr>
  <td nowrap><code>│   │   │   ├── public_subset.csv</code></td>
  <td>CSV with 1 column of <code>row_id, True or False</code> indicating if the row should be used when calculating public leaderboard score.</td>
</tr>
<tr>
  <td nowrap><code>│   │   │   └── test_set_labels.csv</code></td>
  <td>The labels for the test set.</td>
</tr>
<tr>
  <td nowrap><code>│   │   └── public</code></td>
  <td>Data that is released to competitors</td>
</tr>
<tr>
  <td nowrap><code>│   │       ├── pandas_read_csv_kwargs.json</code></td>
  <td> If the <code>pandas.read_csv</code> function needs extra kwargs, they go in here.</td>
</tr>
<tr>
  <td nowrap><code>│   │       ├── submission_format.csv</code></td>
  <td>The submission format. Should look exactly like <code>test_set_labels.csv</code> but with uniform or all 0 entries.</td>
</tr>
<tr>
  <td nowrap><code>│   │       ├── test_set_features.csv</code></td>
  <td>The features for the test set of the competition.</td>
</tr>
<tr>
  <td nowrap><code>│   │       ├── training_set_features.csv</code></td>
  <td>The features for the training set of the competition.</td>
</tr>
<tr>
  <td nowrap><code>│   │       └── training_set_labels.csv</code></td>
  <td>The labels for the training set of the competition.</td>
</tr>
<tr>
  <td nowrap><code>│   ├── interim</code></td>
  <td>A folder for storing cleaned, anonymized, organized data.</td>
</tr>
<tr>
  <td nowrap><code>│   └── raw</code></td>
  <td>The raw data directly from the source.</td>
</tr>
<tr>
  <td nowrap><code>├── data-preparation</code></td>
  <td>A folder to store code that is used to prepare the dataset</td>
</tr>
<tr>
  <td nowrap><code>│   └── 0.1-process-data.ipynb</code></td>
  <td>Notebooks to process raw data into final competition dataset. Should be numbered in sequential order. Can execute all of these with <code>make run-processs</code>.</td>
</tr>
<tr>
  <td nowrap><code>├── pages</code></td>
  <td>Markdown pages with competition content. Contains minimum, but we can always add more pages.</td>
</tr>
<tr>
  <td nowrap><code>│   ├── images</code></td>
  <td>Any images referenced in the markdown files.</td>
</tr>
<tr>
  <td nowrap><code>│   ├── about.md</code></td>
  <td>About the dataset and competition sponsor (non-technical background context).</td>
</tr>
<tr>
  <td nowrap><code>│   ├── home.md</code></td>
  <td>Landing page for the competition. Keep it short and visual.</td>
</tr>
<tr>
  <td nowrap><code>│   └── problem_description.md</code></td>
  <td>Codebook for the dataset used in the competition and technical documentation.</td>
</tr>
<tr>
  <td nowrap><code>├── references</code></td>
  <td>Any pdf or other reference materials about the data or competition.</td>
</tr>
<tr>
  <td nowrap><code>├── Makefile</code></td>
  <td>Relevant commands for preparing a competition.</td>
</tr>
<tr>
  <td nowrap><code>├── README.md</code></td>
  <td>The readme for the project</td>
</tr>
<tr>
  <td nowrap><code>└── requirements.txt</code></td>
  <td>Any Python requirements for executing the code in <code>data-preparation</code> and <code>benchmark</code>.</td>
</tr>

</tbody>
</table>

Commands
------------
Run `make` at the commandline for a list of possible commands.


Steps to create a competition
------------

 - [ ] Download original data to the `data/raw` folder. If this can be automated, add a notebook or script that downloads the data.
 - [ ] If any data file is larger than 40MB, create an S3 bucket for storing the data and keep the data folder out of git. This is the default, but you can change for small datasets.


 - [ ] Do any data cleaning, merging, anonymization and obfuscation in a jupyter notebook in the `data-preparation` folder. Notebooks should be sequentially ordered and execute (see `make run-process`). Resulting dataset goes in `data/interim`.
 - [ ] Split into training sets and test sets as appropriate, results go in `data/final`. These are what will be used in the competition.


 - [ ] Create home and about pages for the competition.
 - [ ] Create documentation about the dataset id `pages/problem_description.md`


 - [ ] Decide on a metric for the competition. If it is not a standard metric, implement it in a standalone `.py` file with tests that confirm its validity.
 - [ ] Create a benchmark notebook with a first pass algorithm for solving the problem. See `make edit-benchmark`.
