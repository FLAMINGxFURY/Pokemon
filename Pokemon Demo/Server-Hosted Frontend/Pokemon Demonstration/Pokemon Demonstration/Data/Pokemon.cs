namespace Pokemon_Demonstration.Data {
    public class Pokemon {
        public int Id { get; set; }
        public string Name { get; set; }
        public string ImageUrl { get; set; }

        public override string ToString() {
            return $"#{Id} {Name[0].ToString().ToUpper()}{new string(Name.Skip(1).ToArray())}";
        }
    }
}
