elements = ["chip8", "cpu"]

def test_all_elements() -> None:
    for e in elements:
        print(e)
        exec(
            f"from tests.{e}_test import test_all;"
            "test_all()"
        )
    print("end")

test_all_elements()