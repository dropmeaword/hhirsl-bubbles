## BUBBLES DRIVER

This is the driver code for the Bubbles installation, a work by Hrvoje Hirsl. 
This code is authored by Luis Rodil-Fernandez.

## Testing the driver
To test that the driver is working as expected you can use the test facility, which will set a new pattern in the elements of the installation every two seconds. The sequence is defined in a plain text file, one line per sequence. The character '#' defines an active component, the character '-' defines an inactive component.

    $ python --test --sequence sequence.txt

## Running the driver
To run the driver in listening mode, run the following command:

    $ python bubbles.py --listen-port 12345

This will set the driver to listen to OSC messages on the port specified.