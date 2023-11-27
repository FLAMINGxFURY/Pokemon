using System.Text;
using System.Text.Json;
using Pokemon_Demonstration.Data;

namespace Pokemon_Demonstration.Services {
	public class FileAPIService : IPokeAPIService {
		
		private HttpClient httpClient;
		protected virtual string BASE_ADDR => "http://localhost:80";


        public FileAPIService() { 
			httpClient = new HttpClient();
		}
		
		public async Task<int> GetPokemonCount() {
			var apiCountResponse = await httpClient.GetFromJsonAsync<JsonElement>($"{BASE_ADDR}/count");
			return apiCountResponse.GetInt32();
		}

		public async Task<Pokemon> GetPokemon(int id) {
			var apiResponse = await httpClient.GetFromJsonAsync<JsonElement>($"{BASE_ADDR}/pokemon/{id}");

			return new Pokemon {
				Id = id,
				Name = apiResponse.GetProperty("name").GetString(),
				ImageUrl = apiResponse.GetProperty("imageurl").GetString()
			};
		}

		public async Task PostPokemon(Pokemon pokemon)
		{
			try
			{
				string json = '{' + $"\"id\":\"{pokemon.Id}\",\n" +
									$"\"name\":\"{pokemon.Name}\",\n" +
									$"\"imageurl\":\"{pokemon.ImageUrl}\"" + '}';

				StringContent JsonContent = new StringContent(json, Encoding.UTF8, "application/json");

				await httpClient.PostAsync($"{BASE_ADDR}/pokemon", JsonContent);
			}
			catch (HttpRequestException ex)
			{
				Console.WriteLine("Failed to post the Pokemon. The Pokemon may already exist. \n" + ex.Message);
			}
		}

		public async Task DeletePokemon(int id) {
			await httpClient.DeleteAsync($"{BASE_ADDR}/pokemon/{id}");
		}
	}
}
