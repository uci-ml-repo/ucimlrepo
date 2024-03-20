import unittest
# from ucimlrepo import list_available_datasets, fetch_ucirepo
from ucimlrepo import fetch_ucirepo, list_available_datasets

class TestMLRepo(unittest.TestCase):
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
           fetch_ucirepo(id=1, name='Abalone')

        with self.assertRaises(ValueError):
           fetch_ucirepo()

        with self.assertRaises(ValueError):
           fetch_ucirepo(id='Abalone')

        with self.assertRaises(ValueError):
           fetch_ucirepo(name=1)

    def test_list(self):
      with self.assertRaises(ValueError):
        list_available_datasets(area='health and medicin')

      with self.assertRaises(ValueError):
        list_available_datasets(filter='abc')

      with self.assertRaises(ValueError):
        list_available_datasets(search='')

      list_available_datasets(area='climate and environment')  
      #  list_available_datasets(filter='python', area='climate and environment')  
      #  list_available_datasets(search='nino', area='climate and environment')  


    def test_nonexistent_dataset(self):
       with self.assertRaises(Exception):
          fetch_ucirepo(id=2000)

    def test_unavailable_dataset(self):
        with self.assertRaises(Exception):
          fetch_ucirepo(id=34)

    def test_heart_disease(self):
      heart_disease = fetch_ucirepo(id=45)
      # print(heart_disease.attributes)
      # print(heart_disease.data.original.head())

      self.assertEqual(heart_disease.metadata.uci_id, 45)
      self.assertEqual(heart_disease.metadata.repository_url, 'https://archive.ics.uci.edu/dataset/45/heart+disease')

      # attribute metadata should have been moved
      self.assertIsNone(heart_disease.metadata.variables)
      self.assertIsNone(heart_disease.attributes)
      
      # dataset has no IDs
      self.assertIsNone(heart_disease.data.ids)

      self.assertEqual(heart_disease.data.features.shape, (303, 13))
      self.assertEqual(heart_disease.data.targets.shape, (303, 1))

      self.assertEqual(heart_disease.variables['name'][0], 'age')
        

if __name__ == '__main__':
  unittest.main()
