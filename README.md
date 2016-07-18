# RegisterGen #

RegisterGen is a generator for C++ code that simplifies access to
hardware registers. It is intended to be mainly used during debugging.

Bit fields and structures are usually used in order to get access to
block of registers and fields. But often some registers or fields are
missing from a manufactures library. If one decides to write access
structures by hand then he must define in 3 separate places: field
structure; addresses and offsets; constants for field values;
(optionally) textual register description and print functions. That is
such utility code is spread out and contains a lot of boiler plate.
This program reads register description in JSON format and generates
C++ code that solves all these problems.

## Example ##

Sample configuration:

```json
{[
  {
    "section": "Register section",
    "address": "0x100000",
	"registers": [
	  { "name": "DEVSTAT",
	    "offset": "0x100",
		"address": "0x80012300",
		"fields": [
		  { "name": "BOOTMODE", "first": 1, "last": 13,
		    "values": [
			  { "name": "I2C", "value": 1 }
			]
		  }
	    ]
	  }
	]
  }
]}
```

Generated code use:

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

Generated code:

```c++
struct DEVSTAT {
  static const std::size_t address = 0x02620020;

  static uint32_t get() {
    return *(reinterpret_cast<volatile uint32_t *>(address));
  }

  static uint32_t set(uint32_t new_value) {
    *(reinterpret_cast<volatile uint32_t *>(address)) = new_value;
    return *(reinterpret_cast<volatile uint32_t *>(address));
  }

  uint32_t value;

  DEVSTAT() : value(get()) {}

  explicit DEVSTAT(uint32_t new_value) {
    set(new_value);
  }

  operator std::size_t() const {
    return value;
  }

  uint32_t BOOTMODE() {
    return GetRegisterField(address, 1, 13);
  }
};
```

