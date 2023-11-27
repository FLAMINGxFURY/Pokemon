using System.Text.Json;
using Pokemon_Demonstration.Data;

namespace Pokemon_Demonstration.Services {
	public class PokeAPIService : IPokeAPIService {
		
		private HttpClient httpClient;

		public PokeAPIService()
		{
			httpClient = new HttpClient();
		}

		public async Task<int> GetPokemonCount() {
			//Get the total number of current pokemon from the API
			var apiCountResponse = await httpClient.GetFromJsonAsync<JsonElement>("https://pokeapi.co/api/v2/pokemon-species?limit=0");
			return apiCountResponse.GetProperty("count").GetInt32();
		}

		/// <summary>
		/// Returns a <see cref="Pokemon"/> given it's integer-based ID
		/// </summary>
		/// <param name="id"><see cref="Pokemon"/>'s ID</param>
		/// <returns>Serialized <see cref="Pokemon"/> Object</returns>
		public async Task<Pokemon> GetPokemon(int id) {
			var apiResponse = await httpClient.GetFromJsonAsync<JsonElement>($"https://pokeapi.co/api/v2/pokemon-species/{id}");

			return new Pokemon {
				Id = id,
				Name = apiResponse.GetProperty("name").GetString(),
				ImageUrl = $"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
			};
		}
	}
}
