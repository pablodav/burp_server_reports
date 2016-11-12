from ..lib.is_up import is_up

def test_isupok():
    assert is_up('localhost')
        
def test_isupfail():
    assert not is_up('nohost')

def test_isupfeedbackok():
    assert is_up('localhost', give_feedback=True)

def test_isupfeedbackfail():
    assert not is_up('nohost', give_feedback=True)

