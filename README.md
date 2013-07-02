# RegisterGen #

Code generator for hardware registers access.

The basic idea is to take a JSON description of hardware registers and
generate C++ code for read/write/print.

Features:
- read/write register values and fields,
- only writable fields can be changed,
- print register values and optionally all fields,
- values of fields can be set and printed using names,
- registers are singletons
- the register object should not have a state

## Example usage ##

Generated code can be used in the following way:

```c++
#include <c66x_registers.h>

int main() {
    uint32_t old_value = c66x_registers::DEVSTAT();
	uint32_t new_value = c66x_registers::DEVSTAT(0x0001);
    uint32_t new_value2 = DEVSTAT().BOOTMODE(c66x_registers::I2C)
	                          .PCIESSEN(0).PACLKSEL(0);

	uint32_t old_field = c66x_registers::DEVSTAT().BOOTMODE();
	uint32_t new_value = c66x_registers::DEVSTAT().BOOTMODE(c66x_registers::I2C);

    std::cout << c66x_registers::DEVSTAT().to_string();
	std::cout << c66x_registers::DEVSTAT().to_string(c66x_registers::VERBOSE);
	std::cout << c66x_registers::DEVSTAT.name();
	std::cout << c66x_registers::DEVSTAT().BOOTMODE().description();
}
```


