
class PokemonService:

    def validar_nombre_trainer(self,name):
        if (len(name) >= 3 and len(name) <= 15):
            return True
        else:
            return False
