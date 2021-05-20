import unittest

from starlette.testclient import TestClient

from pcacontroller import app


class TestAPI(unittest.TestCase):
    client = TestClient(app)

    def setUp(self) -> None:
        return

    def test_all_laws(self):
        response = self.client.get("/api/laws")
        assert response.status_code == 200
        assert response.json() == {"Laws": ['commutativity', 'de_morgan', 'idempotence', 'implication', 'involution',
                                            'maximum', 'minimum']}

    def test_partial_application(self):
        prop = 'not not Q or P?methods=involution'
        response = self.client.get(f"/api/partial/{prop}")
        assert response.status_code == 200
        assert response.json() == {'Result': '(Q ∨ P)'}

    def test_exercise_eval(self):
        q_prop = 'not (Q or P)?methods=de_morgan,involution&t_prop=A or B'
        response = self.client.get(f"/api/exercises/eval/{q_prop}")
        assert response.status_code == 200
        assert response.json() == {'Result_Prop': '(¬ Q ∧ ¬ P)',
                                   'Result': False}
        q_prop = 'not (Q or P)?methods=de_morgan,involution&t_prop=not Q and not P'
        response = self.client.get(f"/api/exercises/eval/{q_prop}")
        assert response.json() == {'Result_Prop': '(¬ Q ∧ ¬ P)',
                                   'Result': True}

    def test_sections_ex(self):
        section = 'INVOLUTION'
        response = self.client.get(f"/api/exercises/{section}")
        assert response.status_code == 200
        assert response.json() == {"Exercises": [
            {"question": "Using the Involution law, which removes double negations, simplify the propositions below",
             "eval_methods": ["involution"], "props": ["not not A", "not (not not (Q or not not P))"]}]}

    def test_ex_sections(self):
        response = self.client.get(f"/api/exercises")
        assert response.status_code == 200
        assert response.json() == {
            "Sections": ['SATISFIABLE', 'TAUTOLOGY', 'CONTRADICTION', 'COMMUTATIVITY', 'IDEMPOTENCE', 'INVOLUTION',
                         'MAX_MIN', 'DE_MORGAN', 'IMPLICATION', 'COMBINATIONS']
        }

    def test_calc_prop(self):
        prop = 'not not Q or P'
        response = self.client.get(f"/api/calc/{prop}")
        assert response.status_code == 200
        assert response.json() == {
            "Proposition": "(¬ (¬ Q) ∨ P)",
            "Satisfiable": True,
            "Tautology": False,
            "Contradiction": False,
            "Variables": ["P", "Q"],
            "Interpretations": [[False, False, False], [False, True, True], [True, False, True],
                                [True, True, True]]
        }


if __name__ == '__main__':
    unittest.main()
