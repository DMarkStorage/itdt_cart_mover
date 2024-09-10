# `itdt_cart_mover`

A Python script for managing data cartridges within storage systems. It uses ITDT commands to retrieve cartridge information, map devices to libraries, and move cartridges to specific slots.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required Python packages:
    ```bash
    pip install subprocess pandas docopt prettytable
    ```

## Usage

### Command-line Options

- `-L <LIB> --cartridges`: Retrieve information about the cartridges in the specified library.
- `-L <LIB> -C <CARTRIDGE> --moveToSlot`: Move the specified cartridge to a slot in the specified library.
- `--version`: Display the version of the script.
- `-h | --help`: Show the help message and exit.

### Examples

1. **Retrieve Cartridge Information**
    ```bash
    python move_cart.py -L 1 --cartridges
    ```

2. **Move Cartridge to Slot**
    ```bash
    python move_cart.py -L 1 -C <CARTRIDGE_ID> --moveToSlot
    ```

## Notes

- Ensure that the `device_scan` command is available on your system and correctly configured.
- Replace `<CARTRIDGE_ID>` with the actual ID of the cartridge you want to move.

## License

This project is licensed under the MIT License.
