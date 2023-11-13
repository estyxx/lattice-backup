# Lattice Competency Backup Tool

<p align="center">
  <img src="lattice_backup.png" width="200" height="200">
</p>

This project is designed to interact with the Lattice GraphQL API to query and back up user competencies. It allows you to export the competency data for archival or analysis purposes.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management and running the project

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/estyxx/lattice-backup.git
cd lattice-backup
```

Install the project dependencies using Poetry:

```bash
poetry install
```

## Configuration

Before running the script, you need to set up your environment variables by creating a `.env` file. An example file `.env.example` is provided in the repository.

### Setting up the .env file

Copy the `.env.example` to a new file named `.env`.

```bash
cp .env.example .env
```

Fill in the `ACCESS_TOKEN` and `LATTICE_USER_ENTITY_ID` with your own values obtained from Lattice.

### Obtaining ACCESS_TOKEN

1. Open your web browser and log into your Lattice account.
2. Open the browser's developer tools and go to the Network tab.
3. Filter for `/graphql/` to find a call to the GraphQL API.
4. Look in the request Headers or the Cookies to find the `access_token`. It should look like `access_token=...;`.

### Finding LATTICE_USER_ENTITY_ID

1. In the developer tools under the Network tab, look for any GraphQL API call payloads.
2. Find the request payload containing `userEntityId: ...` in the variables.

## Running the Script

Once you have your `ACCESS_TOKEN` and `LATTICE_USER_ENTITY_ID`, you can run the script:

```bash
poetry run backup
```

## Backup Options

By default, the script will save the responses `.json` data in the `./backup` directory. You can control the save behavior with the following command line options:

- `--save`: Enables save (this is the default behavior).
- `--no-save`: Disables save.

For example, to disable save:

```bash
poetry run backup --no-save
```

## Data Backup Details

The Lattice Competency Backup Tool captures and saves the following types of data:

### User Competencies

- **Competency Data**: Each competency includes the name, description and 'designation' aka 'Opportunity' or 'Strength'.
- **Current Job Level**: The current level of the user within their career track, including the name and description.
- **Next Job Level**: The next level within the user's career track, including the name and description.
- **Comments**: Comments are captured for each competency, including the commenter's name, the date of the comment, and the comment text itself.

### Growth Areas

- **Growth Area Data** (currently not printed, only saved)

All the above data is saved in JSON format in the `./backup` directory. The growth area data is currently only saved and not printed to the console.

## Important Notes

- Do not share your `ACCESS_TOKEN` or `LATTICE_USER_ENTITY_ID` as they are sensitive information that can grant access to your personal data on Lattice.

## Contributing

If you'd like to contribute to the project, please fork the repository and create a pull request with your changes.
