import base64
from arsenal.forensics.decode import desfa, desfa_straturi, ghici_strat, sparge_xor


def test_ghici_strat():
    assert ghici_strat("%2Fetc") == "url"
    assert ghici_strat("48656c6c6f") == "hex"
    assert ghici_strat("U2FsdXQ=") == "base64"


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_straturi_multiple():
    codat = base64.b64encode(b"FLAG{ok}".hex().encode()).decode()
    straturi, rez = desfa_straturi(codat)
    assert straturi == ["base64", "hex"]
    assert rez == "FLAG{ok}"


def test_xor_brute():
    criptat = bytes(b ^ 0x80 for b in b"FLAG{test_xor}")
    k, clar = sparge_xor(criptat)
    assert k == 0x80
    assert clar == "FLAG{test_xor}"