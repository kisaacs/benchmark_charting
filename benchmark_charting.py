from data_model import ChartingDataModel, ChartingDataManager


def test_data_model():
    db = ChartingDataModel()
    db.add_settings('blazemark_base_path', '/home/sayefsakin/blaze-3.8/blazemark/bin/complex1')
    db.add_settings('blazemark_argument', '-only-blaze')

    param_list = []
    param_list.append({"name": "threads", "values": [8]})
    param_list.append({"name": "block_size", "values": [10, 20, 30, 40, 50, 60]})
    param_list.append({"name": "chunk_size", "values": [3, 5]})
    ch = ChartingDataManager("admin")
    ch.add_new_measurements(db, param_list, 1)
    # ch.add_chart_legends(db,"chunk_size", 3)
    # ch.add_chart_legends(db,"Mflops", 50)
    # ch.add_chart_legends(db,"threads", 8)
    # ch.add_chart_legends(db,"block_size", 10, 20, 5)
    # ch.add_chart_x_axis(db,"chunk_size", 3)

    # still need to do some work to safely update x_values and legends
    # n_uid = c.create_chart("my_chart")
    # c.add_new_datapoint(n_uid, "blazemark")


if __name__ == '__main__':
    print("Hello from benchmark charting")
    test_data_model()
