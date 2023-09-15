import unittest
# from ucimlrepo.fetch import fetch, list_available_datasets
from ucimlrepo import list_available_datasets, fetch_ucirepo

class TestMLRepo(unittest.TestCase):
    # def test_invalid_inputs(self):
    #     self.assertRaises(fetch_mlrepo(id=1, name='Abalone'))
    #     self.assertRaises(fetch_mlrepo())
    #     self.assertRaises(fetch_mlrepo(id='Abalone'))
    #     self.assertRaises(fetch_mlrepo(name=1))

    # def test_list(self):
    #    list_available_datasets()

    # def test_nonexistent_dataset(self):
    #    self.assertRaises(fetch_mlrepo(id=2000))

    # def test_unavailable_dataset(self):
    #    self.assertRaises(fetch_mlrepo(id=53))

    def test_heart_disease(self):
      heart_disease = fetch_ucirepo(id=565)
      print(heart_disease.variables)
      print(heart_disease.metadata.num_features)

      # self.assertEqual(heart_disease.metadata.uci_id, 45)
      # self.assertEqual(heart_disease.metadata.repository_url, 'https://archive.ics.uci.edu/dataset/45/heart+disease')

      # # attribute metadata should have been moved
      # self.assertIsNone(heart_disease.metadata.attributes)
      
      # # dataset has no IDs
      # self.assertIsNone(heart_disease.data.ids)

      # self.assertEqual(heart_disease.data.features.shape, (303, 13))
      # self.assertEqual(heart_disease.data.targets.shape, (303, 1))

      # self.assertEqual(heart_disease.attributes['name'][0], 'age')

       
        

if __name__ == '__main__':
  unittest.main()


# conda activate pandas_env
# python src/test.py