using Pokemon_Demonstration.Data;

namespace Pokemon_Demonstration.Services {
	public interface IPokeAPIService {
		Task<int> GetPokemonCount();
		Task<Pokemon> GetPokemon(int id);
	}
}
