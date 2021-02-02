from ..transformation.proximity import Proximity


class InfectedContacts:
    @staticmethod
    def infected_ids(user_id_):
        Infected_nodes_ = Proximity.fetch_ids_in_close_proximity(user_id_)

        unique_infected_Contact_List = []
        for el in Infected_nodes_:
            unique_infected_Contact_List.append(el[0])
        unique_infected_Contact_List = list(set(unique_infected_Contact_List))
        return unique_infected_Contact_List

    @staticmethod
    def infected_ids_before_date(user_id_, date_):
        Infected_nodes_ = Proximity.fetch_ids_in_close_proximity_before_date(user_id_, date_)
        return Infected_nodes_
